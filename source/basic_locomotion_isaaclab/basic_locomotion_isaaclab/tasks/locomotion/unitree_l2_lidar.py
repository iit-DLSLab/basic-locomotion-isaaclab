"""Unitree L2 LiDAR model.

The scan pattern, timing and range errors are identified from a Go2 rosbag (``/utlidar/cloud``, frame
``utlidar_lidar``) recorded with the robot standing on flat ground:

* the laser fires every ~7.73 us along arcs of 300 samples that go from the horizon, over the zenith (+z of the
  L2 frame) and down to the opposite horizon (elevation in [0, 90] deg on both sides, ~2.3 ms per arc);
* the arcs repeat at 215.8 Hz, while the scanning head turns around +z at 1573 deg/s (4.37 rev/s), so the pattern
  never repeats exactly;
* the driver publishes chunks of 64.9 ms (15.4 Hz, ~4175 points, 99.7% of the firing slots return a point) stamped
  with the time of their first point; every point carries its firing time and is expressed in the L2 frame at that
  time (no motion compensation);
* range noise is small and repeatable (~1 mm at 0.3 m, ~5 mm beyond 1 m, 1 mm resolution), but the ranges have
  a smooth systematic error of a few cm that oscillates with the distance; no point below 0.2 m is published.
"""

from __future__ import annotations

import math
from collections.abc import Callable, Sequence

import torch
import warp as wp

import isaaclab.utils.math as math_utils
from isaaclab.utils.configclass import configclass


def unitree_l2_scan(
    cfg: "UnitreeL2PatternCfg", t_end: torch.Tensor
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """Firing slots of the L2 message that ends at ``t_end``.

    Args:
        cfg: The L2 pattern configuration.
        t_end: Scanner clock [s] at the end of each message. Shape is (N,), float64.

    Returns:
        The ray directions in the L2 frame. Shape is (N, R, 3).
        The firing times [s] relative to the message stamp (the start of the message). Shape is (N, R), float64.
        Whether each slot falls inside the message. Shape is (N, R).
    """
    device = t_end.device
    t_start = t_end - cfg.message_period
    # every arc that may overlap the message, the slots outside of it are flagged as invalid
    arcs_per_message = int(math.ceil(cfg.message_period * cfg.arc_frequency)) + 1
    arc_ids = torch.floor(t_start * cfg.arc_frequency)[:, None] + torch.arange(
        arcs_per_message, dtype=torch.float64, device=device
    )
    sample_ids = torch.arange(cfg.samples_per_arc, dtype=torch.float64, device=device)
    t = (arc_ids[:, :, None] / cfg.arc_frequency + sample_ids * cfg.sample_period).flatten(1)
    valid = (t >= t_start[:, None]) & (t < t_end[:, None])

    # azimuth of the arc, the head keeps turning while the arc is drawn
    azimuth = torch.remainder(t * math.radians(cfg.rotation_speed), 2.0 * math.pi).float()
    # angle along the arc: 0 at the horizon, 90 deg at the zenith, 180 deg at the opposite horizon
    half_span = 0.5 * (cfg.samples_per_arc - 1)
    x = (sample_ids.float() - half_span) / half_span
    arc_angle = torch.deg2rad(90.0 + sum(c * x ** (2 * i + 1) for i, c in enumerate(cfg.arc_angle_coefficients)))
    arc_angle = arc_angle.repeat(arcs_per_message)

    cos_arc = torch.cos(arc_angle)
    ray_directions = torch.stack(
        (cos_arc * torch.cos(azimuth), cos_arc * torch.sin(azimuth), torch.sin(arc_angle).expand_as(azimuth)), dim=-1
    )
    return ray_directions, t - t_start[:, None], valid


def unitree_l2_non_repetitive_pattern(
    cfg: "UnitreeL2PatternCfg", device: str
) -> tuple[torch.Tensor, torch.Tensor]:
    """Rays of the first L2 message. :class:`UnitreeL2Lidar` moves them along the scan at every update."""
    t_end = torch.tensor([cfg.message_period], dtype=torch.float64, device=device)
    ray_directions, _, _ = unitree_l2_scan(cfg, t_end)
    ray_directions = ray_directions[0]
    return torch.zeros_like(ray_directions), ray_directions


@configclass
class UnitreeL2PatternCfg:
    """Configuration for the Unitree L2 non-repetitive LiDAR scan pattern and its range errors.

    The rays are defined in the L2 frame (hemisphere around +z), the mounting is set with the sensor offset.
    """

    func: Callable = unitree_l2_non_repetitive_pattern

    # scan pattern and timing

    sample_period: float = 7.726e-6
    """Time between two consecutive firings along an arc in seconds."""

    samples_per_arc: int = 300
    """Number of firings in an arc (horizon -> zenith -> opposite horizon)."""

    arc_frequency: float = 215.83
    """Frequency of the arcs (vertical scan frequency) in Hz."""

    rotation_speed: float = 1573.1
    """Rotation speed of the scanning head around the +z axis of the L2 frame in deg/s."""

    arc_angle_coefficients: tuple[float, ...] = (78.98, 10.92)
    """Odd polynomial (deg) of the angle along the arc, 90 + c1 * x + c3 * x^3, with x in [-1, 1] over the arc."""

    message_period: float = 0.0649
    """Duration of the scan published in each message in seconds (15.4 Hz)."""

    # range model

    min_range: float = 0.2
    """Points closer than this distance in meters are not published."""

    dropout_probability: float = 0.0034
    """Probability that a firing slot hitting a surface does not return a point."""

    range_noise_std_per_meter: float = 0.0045
    """Standard deviation of the white range noise per meter of distance."""

    range_noise_std_range: tuple[float, float] = (0.001, 0.006)
    """Clipping range of the standard deviation of the white range noise in meters."""

    range_resolution: float = 0.001
    """Range quantization in meters. Set to 0 to disable it."""

    range_bias_amplitude_range: tuple[float, float] = (0.0, 0.04)
    """Range of the amplitude in meters of the systematic range error, sampled at every reset.

    The error is ``amplitude * sin(2 * pi * distance / wavelength + phase)``.
    """

    range_bias_wavelength_range: tuple[float, float] = (0.1, 0.5)
    """Range of the wavelength in meters of the systematic range error, sampled at every reset."""

    simulate_motion_distortion: bool = True
    """Whether each ray is cast from the sensor pose at its firing time instead of the pose at the end of the message.

    The pose is interpolated between the last two updates, so the sensor must be updated every message.
    """


class _UnitreeL2LidarMixin:
    """Moves the rays of a multi-mesh ray caster along the L2 scan and applies the L2 range errors.

    Besides :attr:`data`, whose hits are in world frame, the sensor exposes the message as published by the robot:

    * :attr:`points_l2`: points in the L2 frame at their firing time. Shape is (N, R, 3).
    * :attr:`point_times`: firing times [s] relative to the message stamp. Shape is (N, R).
    * :attr:`point_valid`: whether each slot returned a point. Shape is (N, R).

    Slots without a point are set to inf, as in :attr:`data`.
    """

    def reset(self, env_ids: Sequence[int] | None = None, env_mask: wp.array | None = None):
        super().reset(env_ids, env_mask)
        if env_ids is not None:
            env_ids = torch.as_tensor(env_ids, device=self._device)
        elif env_mask is not None:
            env_ids = wp.to_torch(env_mask).nonzero(as_tuple=False).squeeze(-1)
        else:
            env_ids = torch.arange(self._view_count, device=self._device)
        self._sample_scanner_state(env_ids)

    def _initialize_rays_impl(self):
        super()._initialize_rays_impl()
        if self.cfg.ray_alignment != "base":
            raise ValueError(f"UnitreeL2Lidar requires ray_alignment='base'. Received: {self.cfg.ray_alignment}.")
        num_envs, device = self._view_count, self._device

        self._offset_quat_l2 = torch.tensor(list(self.cfg.offset.rot), device=device).repeat(self.num_rays, 1)
        # free-running scanner clock, range error and pose at the last update of each sensor
        self._scanner_clock = torch.zeros(num_envs, dtype=torch.float64, device=device)
        self._range_bias_amplitude = torch.zeros(num_envs, device=device)
        self._range_bias_wavenumber = torch.zeros(num_envs, device=device)
        self._range_bias_phase = torch.zeros(num_envs, device=device)
        self._last_update_time = torch.full((num_envs,), -math.inf, dtype=torch.float64, device=device)
        self._last_update_pos_w = torch.zeros(num_envs, 3, device=device)
        self._last_update_quat_w = torch.zeros(num_envs, 4, device=device)
        self._firing_lag = torch.zeros(num_envs, self.num_rays, device=device)
        self._updating_env_ids = None

        self.points_l2 = torch.full((num_envs, self.num_rays, 3), math.inf, device=device)
        self.point_times = torch.zeros(num_envs, self.num_rays, device=device)
        self.point_valid = torch.zeros(num_envs, self.num_rays, dtype=torch.bool, device=device)
        self._sample_scanner_state(torch.arange(num_envs, device=device))

    def _sample_scanner_state(self, env_ids: torch.Tensor):
        pattern_cfg = self.cfg.pattern_cfg
        num_envs = len(env_ids)
        self._scanner_clock[env_ids] = 1000.0 * torch.rand(num_envs, dtype=torch.float64, device=self._device)
        self._range_bias_amplitude[env_ids] = math_utils.sample_uniform(
            *pattern_cfg.range_bias_amplitude_range, (num_envs,), device=self._device
        )
        wavelength = math_utils.sample_uniform(
            *pattern_cfg.range_bias_wavelength_range, (num_envs,), device=self._device
        )
        self._range_bias_wavenumber[env_ids] = 2.0 * math.pi / wavelength
        self._range_bias_phase[env_ids] = math_utils.sample_uniform(0.0, 2.0 * math.pi, (num_envs,), self._device)
        self._last_update_time[env_ids] = -math.inf

    def _update_buffers_impl(self, env_mask: wp.array):
        env_ids = wp.to_torch(env_mask).nonzero(as_tuple=False).squeeze(-1)
        if len(env_ids) == 0:
            return super()._update_buffers_impl(env_mask)
        pattern_cfg = self.cfg.pattern_cfg

        # rays of the message that ends now
        t_end = self._scanner_clock[env_ids] + wp.to_torch(self._timestamp)[env_ids].double()
        ray_directions_l2, point_times, in_message = unitree_l2_scan(pattern_cfg, t_end)
        self.ray_directions.torch[env_ids] = math_utils.quat_apply(
            self._offset_quat_l2.expand(len(env_ids), -1, -1), ray_directions_l2
        )
        self._firing_lag[env_ids] = (pattern_cfg.message_period - point_times).float()
        self._updating_env_ids = env_ids
        self._updating_t_end = t_end

        super()._update_buffers_impl(env_mask)
        self._apply_range_model(env_ids, ray_directions_l2, point_times, in_message)

        self._last_update_time[env_ids] = t_end
        self._last_update_pos_w[env_ids] = wp.to_torch(self._data._pos_w)[env_ids]
        self._last_update_quat_w[env_ids] = wp.to_torch(self._data._quat_w)[env_ids]
        self._updating_env_ids = None

    def _update_ray_infos(self, env_mask: wp.array):
        super()._update_ray_infos(env_mask)
        env_ids = self._updating_env_ids
        if env_ids is None or not self.cfg.pattern_cfg.simulate_motion_distortion:
            return

        # cast each ray from the pose at its firing time, interpolated between the last update and now
        elapsed = self._updating_t_end - self._last_update_time[env_ids]
        interpolable = elapsed <= 2.0 * self.cfg.pattern_cfg.message_period
        env_ids, elapsed = env_ids[interpolable], elapsed[interpolable].float()
        if len(env_ids) == 0:
            return
        pos_w = wp.to_torch(self._data._pos_w)[env_ids]
        quat_w = wp.to_torch(self._data._quat_w)[env_ids]
        rotation_to_last = math_utils.axis_angle_from_quat(
            math_utils.quat_mul(math_utils.quat_inv(quat_w), self._last_update_quat_w[env_ids])
        )
        fraction = (self._firing_lag[env_ids] / elapsed[:, None]).clamp(max=1.0).unsqueeze(-1)
        rotation = fraction * rotation_to_last[:, None, :]
        quat_w = quat_w[:, None, :].expand(-1, self.num_rays, -1)

        ray_starts = self.ray_starts.torch[env_ids]
        ray_starts_w = wp.to_torch(self._ray_starts_w)
        ray_starts_w[env_ids] += fraction * (self._last_update_pos_w[env_ids] - pos_w)[:, None, :] + (
            math_utils.quat_apply(quat_w, _rotate(rotation, ray_starts) - ray_starts)
        )
        wp.to_torch(self._ray_directions_w)[env_ids] = math_utils.quat_apply(
            quat_w, _rotate(rotation, self.ray_directions.torch[env_ids])
        )

    def _apply_range_model(
        self,
        env_ids: torch.Tensor,
        ray_directions_l2: torch.Tensor,
        point_times: torch.Tensor,
        in_message: torch.Tensor,
    ):
        pattern_cfg = self.cfg.pattern_cfg
        ray_hits_w = wp.to_torch(self._data._ray_hits_w)
        ray_starts_w = wp.to_torch(self._ray_starts_w)[env_ids]
        ray_directions_w = wp.to_torch(self._ray_directions_w)[env_ids]

        distance = torch.linalg.norm(ray_hits_w[env_ids] - ray_starts_w, dim=-1)
        hit = torch.isfinite(distance)
        distance = torch.where(hit, distance, 0.0)

        noise_std = (pattern_cfg.range_noise_std_per_meter * distance).clamp(*pattern_cfg.range_noise_std_range)
        bias = self._range_bias_amplitude[env_ids, None] * torch.sin(
            self._range_bias_wavenumber[env_ids, None] * distance + self._range_bias_phase[env_ids, None]
        )
        measured = distance + bias + noise_std * torch.randn_like(distance)
        if pattern_cfg.range_resolution > 0.0:
            measured = torch.round(measured / pattern_cfg.range_resolution) * pattern_cfg.range_resolution

        valid = (
            in_message
            & hit
            & (measured >= pattern_cfg.min_range)
            & (torch.rand_like(distance) >= pattern_cfg.dropout_probability)
        ).unsqueeze(-1)
        measured = measured.unsqueeze(-1)
        ray_hits_w[env_ids] = torch.where(valid, ray_starts_w + measured * ray_directions_w, math.inf)
        self.points_l2[env_ids] = torch.where(valid, measured * ray_directions_l2, math.inf)
        self.point_times[env_ids] = point_times.float()
        self.point_valid[env_ids] = valid.squeeze(-1)


def _rotate(rotation: torch.Tensor, vectors: torch.Tensor) -> torch.Tensor:
    """Rotates vectors by rotation vectors (Rodrigues' formula). Shapes are (..., 3)."""
    angle = torch.linalg.norm(rotation, dim=-1, keepdim=True)
    axis = rotation / angle.clamp(min=1e-9)
    cos_angle, sin_angle = torch.cos(angle), torch.sin(angle)
    return (
        vectors * cos_angle
        + torch.cross(axis, vectors, dim=-1) * sin_angle
        + axis * (axis * vectors).sum(dim=-1, keepdim=True) * (1.0 - cos_angle)
    )


class UnitreeL2Lidar:
    """Unitree L2 LiDAR on top of the :class:`~isaaclab.sensors.MultiMeshRayCaster` of the active backend.

    The configuration is a :class:`~isaaclab.sensors.MultiMeshRayCasterCfg` with a :class:`UnitreeL2PatternCfg`
    and ``update_period`` equal to the message period.
    """

    _sensor_classes: dict[type, type] = {}

    def __new__(cls, cfg):
        from isaaclab.sensors import MultiMeshRayCaster

        backend_class = MultiMeshRayCaster.resolve_class(cfg)
        if backend_class not in cls._sensor_classes:
            cls._sensor_classes[backend_class] = type(
                f"UnitreeL2Lidar{backend_class.__name__}", (_UnitreeL2LidarMixin, backend_class), {}
            )
        return cls._sensor_classes[backend_class](cfg)
