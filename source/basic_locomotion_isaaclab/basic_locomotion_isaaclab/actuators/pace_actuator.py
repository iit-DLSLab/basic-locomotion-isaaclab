# © 2025 ETH Zurich, Robotic Systems Lab
# Author: Filip Bjelonic
# Licensed under the Apache License 2.0
#
# Isaac Lab 3 compatible copy of pace_sim2real.utils.PaceDCMotor v0.2.0 (works on PhysX and Newton), with only its
# default delay on the commands. 

from __future__ import annotations

import torch
from collections.abc import Sequence

from isaaclab.actuators import DCMotor, DCMotorCfg, resolve_joint_parameter
from isaaclab.utils.types import ArticulationActions
from isaaclab.utils import DelayBuffer
from isaaclab.utils.configclass import configclass


class PaceDCMotor(DCMotor):
    """Pace DC Motor actuator model with encoder bias and action delay.

    The actuator models a DC motor whose controller receives joint positions in the encoder
    frame by adding a per-joint encoder bias to the true joint positions. In other words,
    the controller operates on biased (encoder) positions rather than the true joint positions.

    A configurable delay (in simulation steps) represents the latency between command calculation and actuation:
    the commanded targets reach the drive late, while the PD controller acts on the current measurements.

    The software implementation is inspired by DelayedPDActuator.
    """

    cfg: PaceDCMotorCfg

    def __init__(self, cfg: PaceDCMotorCfg, *args, **kwargs):
        super().__init__(cfg, *args, **kwargs)
        if isinstance(cfg.encoder_bias, (list, tuple)):
            if len(cfg.encoder_bias) != self.num_joints:
                raise ValueError(
                    f"encoder_bias must have {self.num_joints} elements (one per joint), "
                    f"but got {len(cfg.encoder_bias)}: {cfg.encoder_bias}"
                )
        self.encoder_bias = resolve_joint_parameter(
            cfg.encoder_bias, 0.0, self.joint_names, self._num_envs, self._device
        )

        # one buffer per command signal
        self.delay_buffers = {
            name: DelayBuffer(cfg.max_delay + 1, self._num_envs, device=self._device)
            for name in ("position", "velocity", "effort")
        }
        for buffer in self.delay_buffers.values():
            buffer.set_time_lag(cfg.max_delay, torch.arange(self._num_envs, device=self._device))

    def reset(self, env_ids: Sequence[int]):
        super().reset(env_ids)
        # reset buffers
        for buffer in self.delay_buffers.values():
            try:
                buffer.reset(env_ids)
            except RuntimeError:
                # Isaac Lab 3.0: warp-backed CircularBuffer rejects indexed resets;
                # fall back to a full reset (one-step delay transient for other envs)
                buffer.reset(None)

    def update_encoder_bias(self, encoder_bias: torch.Tensor):
        self.encoder_bias = encoder_bias

    def update_time_lags(self, delay: int | torch.Tensor, env_ids: Sequence[int] | None = None):
        if env_ids is None:
            env_ids = torch.arange(self._num_envs, device=self._device)
        for buffer in self.delay_buffers.values():
            buffer.set_time_lag(delay, env_ids)

    def compute(
        self, control_action: ArticulationActions, joint_pos: torch.Tensor, joint_vel: torch.Tensor
    ) -> ArticulationActions:
        # delay the commanded targets (joint position, velocity and feed-forward effort)
        control_action.joint_positions = self.delay_buffers["position"].compute(control_action.joint_positions)
        control_action.joint_velocities = self.delay_buffers["velocity"].compute(control_action.joint_velocities)
        control_action.joint_efforts = self.delay_buffers["effort"].compute(control_action.joint_efforts)
        # compute actuator model with encoder bias added to joint positions (joint position in encoder frame, not simulation frame)
        return super().compute(control_action, joint_pos - self.encoder_bias, joint_vel)


@configclass
class PaceDCMotorCfg(DCMotorCfg):
    """Configuration for Pace DC Motor actuator model.

    This class extends the base DCMotorCfg with Pace-specific parameters.
    """
    class_type: type = PaceDCMotor
    encoder_bias: dict[str, float] | float | None = 0.0
    max_delay: torch.int | None = 0
