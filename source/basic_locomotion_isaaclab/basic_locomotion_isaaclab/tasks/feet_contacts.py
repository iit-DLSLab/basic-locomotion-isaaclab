"""Foot contact state read by the rewards and the observations.

FeetContacts reads the ContactSensor (the behavior of every task without granular terrain). RFTFeetContacts adds the
3D-RFT sand contact of isaaclab-rft: the RFT force is an external wrench, so the ContactSensor does not see it and a foot
standing in sand would read as airborne. It keeps its own air and contact timers, updated every physics step with the
same rules as the ContactSensor.
"""

from __future__ import annotations

import torch


class FeetContacts:
    """Foot contacts from the ContactSensor, in the order FL, FR, RL, RR."""

    def __init__(self, env):
        self._sensor = env._contact_sensor
        self._ids = env._feet_contact_sensor_ids

    def in_contact(self) -> torch.Tensor:
        """(num_envs, num_feet) bool: contact in the last sensor update."""
        return torch.linalg.norm(self._sensor.data.net_forces_w[:, self._ids, :], dim=-1) > 1.0

    def in_contact_history(self) -> torch.Tensor:
        """(num_envs, num_feet) bool: contact in any update of the sensor history."""
        return self._sensor.data.net_forces_w_history[:, :, self._ids, :].norm(dim=-1).max(dim=1)[0] > 1.0

    def current_air_time(self) -> torch.Tensor:
        return self._sensor.data.current_air_time[:, self._ids]

    def current_contact_time(self) -> torch.Tensor:
        return self._sensor.data.current_contact_time[:, self._ids]

    def last_air_time(self) -> torch.Tensor:
        return self._sensor.data.last_air_time[:, self._ids]

    def last_contact_time(self) -> torch.Tensor:
        return self._sensor.data.last_contact_time[:, self._ids]

    def first_contact(self, dt: float) -> torch.Tensor:
        """(num_envs, num_feet) bool: contact established within the last dt seconds."""
        return self._sensor.compute_first_contact(dt)[:, self._ids]

    def update(self, dt: float) -> None:
        """Called every physics step (the ContactSensor updates itself)."""

    def reset(self, env_ids: torch.Tensor) -> None:
        """Called at reset (the ContactSensor resets itself)."""


class RFTFeetContacts(FeetContacts):
    """Rigid contact (ContactSensor) or sand contact (isaaclab-rft).

    A foot is in sand contact when the RFT force on it exceeds force_threshold [N] or when it is deeper than
    depth_threshold [m] below its sand plane. The depth catches a loaded foot at rest, which pure RFT gives almost no
    force (the force ramps to zero below v_eps). history_length physics steps are kept for in_contact_history.
    """

    def __init__(self, env, rft, force_threshold: float = 1.0, depth_threshold: float = 0.01, history_length: int = 6):
        super().__init__(env)
        if rft.terms is None:
            raise ValueError("RFTFeetContacts reads the foot depth, which needs RFTCfg.terrain_terms = True")
        self._rft = rft
        self._force_threshold = force_threshold
        self._depth_threshold = depth_threshold
        n, nf, dev = env.num_envs, len(self._ids), env.device
        self._contact = torch.zeros(n, nf, dtype=torch.bool, device=dev)
        self._history = torch.zeros(n, max(1, history_length), nf, dtype=torch.bool, device=dev)
        self._current_air_time = torch.zeros(n, nf, device=dev)
        self._current_contact_time = torch.zeros(n, nf, device=dev)
        self._last_air_time = torch.zeros(n, nf, device=dev)
        self._last_contact_time = torch.zeros(n, nf, device=dev)
        self._dt = env.physics_dt

    def _measure(self) -> torch.Tensor:
        sand = self._rft.in_contact(self._force_threshold) | (self._rft.depth > self._depth_threshold)
        if self._rft.sand is not None:
            # partial sand (RFTCfg.sand_fraction < 1): the envs without sand have the rigid contact only
            sand &= self._rft.sand.unsqueeze(1)
        return super().in_contact() | sand

    def update(self, dt: float) -> None:
        # Same rules as the Isaac Lab ContactSensor air time tracking
        self._dt = dt
        contact = self._measure()
        first_contact = (self._current_air_time > 0.0) & contact
        first_detached = (self._current_contact_time > 0.0) & ~contact
        self._last_air_time = torch.where(first_contact, self._current_air_time + dt, self._last_air_time)
        self._current_air_time = torch.where(~contact, self._current_air_time + dt, 0.0)
        self._last_contact_time = torch.where(first_detached, self._current_contact_time + dt, self._last_contact_time)
        self._current_contact_time = torch.where(contact, self._current_contact_time + dt, 0.0)
        self._contact = contact
        self._history = torch.roll(self._history, 1, dims=1)
        self._history[:, 0] = contact

    def reset(self, env_ids: torch.Tensor) -> None:
        for buf in (self._contact, self._history, self._current_air_time, self._current_contact_time,
                    self._last_air_time, self._last_contact_time):
            buf[env_ids] = 0

    def in_contact(self) -> torch.Tensor:
        return self._contact

    def in_contact_history(self) -> torch.Tensor:
        return self._history.any(dim=1)

    def current_air_time(self) -> torch.Tensor:
        return self._current_air_time

    def current_contact_time(self) -> torch.Tensor:
        return self._current_contact_time

    def last_air_time(self) -> torch.Tensor:
        return self._last_air_time

    def last_contact_time(self) -> torch.Tensor:
        return self._last_contact_time

    def first_contact(self, dt: float) -> torch.Tensor:
        # As ContactSensor.compute_first_contact, with half a physics step of tolerance
        return (self._current_contact_time > 0.0) & (self._current_contact_time < dt + 0.5 * self._dt)
