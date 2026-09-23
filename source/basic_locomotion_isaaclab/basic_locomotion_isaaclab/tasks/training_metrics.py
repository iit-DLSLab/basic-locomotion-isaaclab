import torch


@torch.no_grad()
def locomotion_metrics(
    commands: torch.Tensor,
    linear_velocity: torch.Tensor,
    angular_velocity: torch.Tensor,
    projected_gravity: torch.Tensor,
    actions: torch.Tensor,
    previous_actions: torch.Tensor,
    joint_efforts: torch.Tensor,
    joint_velocities: torch.Tensor,
    action_limit: float,
    unclipped_actions: torch.Tensor | None = None,
) -> dict[str, torch.Tensor]:
    """Compute rollout diagnostics that RSL-RL can send to TensorBoard or W&B.

    Velocities and commands use the robot base frame. Mechanical power is the
    sum of absolute joint torque times velocity, not electrical consumption.
    """
    velocity_error = linear_velocity[:, :2] - commands[:, :2]
    tilt = torch.acos((-projected_gravity[:, 2]).clamp(-1.0, 1.0))
    clipping_source = actions if unclipped_actions is None else unclipped_actions
    metrics = {
        "Tracking/vx_mae_mps": velocity_error[:, 0].abs().mean(),
        "Tracking/vy_mae_mps": velocity_error[:, 1].abs().mean(),
        "Tracking/xy_error_mps": velocity_error.norm(dim=-1).mean(),
        "Tracking/yaw_rate_mae_radps": (angular_velocity[:, 2] - commands[:, 2]).abs().mean(),
        "Stability/tilt_rad": tilt.mean(),
        "Stability/vertical_speed_abs_mps": linear_velocity[:, 2].abs().mean(),
        "Actions/absolute_mean": actions.abs().mean(),
        "Actions/change_absolute_mean": (actions - previous_actions).abs().mean(),
        "Actions/clipped_fraction": (clipping_source.abs() > action_limit).float().mean(),
        "Actuation/torque_absolute_mean_Nm": joint_efforts.abs().mean(),
        "Actuation/mechanical_power_abs_W": (joint_efforts * joint_velocities).abs().sum(-1).mean(),
    }
    for axis, index in (("vx", 0), ("vy", 1)):
        metrics[f"Motion/command_{axis}_mps"] = commands[:, index].mean()
        metrics[f"Motion/measured_{axis}_mps"] = linear_velocity[:, index].mean()
    metrics["Motion/command_yaw_rate_radps"] = commands[:, 2].mean()
    metrics["Motion/measured_yaw_rate_radps"] = angular_velocity[:, 2].mean()
    return metrics
