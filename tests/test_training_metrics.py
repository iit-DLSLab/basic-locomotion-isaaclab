import importlib.util
import pathlib
import unittest

import torch


MODULE_PATH = (
    pathlib.Path(__file__).parents[1]
    / "source/basic_locomotion_isaaclab/basic_locomotion_isaaclab/tasks/training_metrics.py"
)
SPEC = importlib.util.spec_from_file_location("training_metrics", MODULE_PATH)
training_metrics = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(training_metrics)
locomotion_metrics = training_metrics.locomotion_metrics


class TrainingMetricsTest(unittest.TestCase):
    def test_units_and_absolute_errors_do_not_cancel(self):
        metrics = locomotion_metrics(
            commands=torch.zeros(2, 3),
            linear_velocity=torch.tensor([[3.0, 4.0, 2.0], [-3.0, -4.0, -2.0]]),
            angular_velocity=torch.tensor([[0.0, 0.0, 0.5], [0.0, 0.0, -0.5]]),
            projected_gravity=torch.tensor([[0.0, 0.0, -1.0], [0.0, 0.0, -1.0]]),
            actions=torch.tensor([[1.0, 0.0], [-1.0, 0.0]]),
            previous_actions=torch.zeros(2, 2),
            joint_efforts=torch.tensor([[2.0, -3.0], [2.0, -3.0]]),
            joint_velocities=torch.tensor([[4.0, 5.0], [4.0, 5.0]]),
            action_limit=1.0,
            unclipped_actions=torch.tensor([[2.0, 0.0], [-2.0, 0.0]]),
        )
        expected = {
            "Tracking/vx_mae_mps": 3.0,
            "Tracking/vy_mae_mps": 4.0,
            "Tracking/xy_error_mps": 5.0,
            "Tracking/yaw_rate_mae_radps": 0.5,
            "Stability/tilt_rad": 0.0,
            "Stability/vertical_speed_abs_mps": 2.0,
            "Actions/clipped_fraction": 0.5,
            "Actuation/torque_absolute_mean_Nm": 2.5,
            "Actuation/mechanical_power_abs_W": 23.0,
            "Motion/measured_vx_mps": 0.0,
        }
        for name, value in expected.items():
            self.assertAlmostEqual(metrics[name].item(), value, msg=name)
        self.assertTrue(all(value.ndim == 0 and torch.isfinite(value) for value in metrics.values()))


if __name__ == "__main__":
    unittest.main()
