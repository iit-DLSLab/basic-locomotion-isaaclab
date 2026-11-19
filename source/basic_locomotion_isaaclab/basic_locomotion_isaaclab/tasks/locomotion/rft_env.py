"""LocomotionEnv on granular terrain (sand), with the 3D-RFT foot contact of isaaclab-rft.

Every physics step the RFT mixin adds the sand force on each foot as an external wrench. On top of it this env:
- reads the foot contacts and air times from the rigid ContactSensor or the sand (RFTFeetContacts), since the
  ContactSensor does not see the RFT force;
- raises the terrain heights of the rewards and observations by the sand height (the height scanners hit the rigid
  terrain under the sand);
- adds the RFT terrain terms (slip, sinkage, bed work, downslope push) of cfg.rft_terrain_reward_scales as separate
  reward terms, logged and published in extras["reward_terms"] like the others.

The config needs an RFTCfg in `rft`, see rft_env_cfg.py.
"""

from __future__ import annotations

import torch

from isaaclab_rft.isaaclab import RFTDirectMixin

from basic_locomotion_isaaclab.tasks.feet_contacts import RFTFeetContacts

from .locomotion_env import LocomotionEnv


class LocomotionRFTEnv(RFTDirectMixin, LocomotionEnv):  # the mixin first

    def __init__(self, cfg, render_mode: str | None = None, **kwargs):
        # The terrain terms are added here, one reward term each, not summed by the mixin
        if cfg.rft.terrain_reward_scales:
            raise ValueError("set the RFT terrain reward weights in cfg.rft_terrain_reward_scales, not in cfg.rft")
        super().__init__(cfg, render_mode, **kwargs)  # builds self.rft after LocomotionEnv.__init__

        self._rft_reward_scales = {k: v for k, v in (cfg.rft_terrain_reward_scales or {}).items() if v != 0.0}
        for term in self._rft_reward_scales:
            self._episode_sums[f"rft_{term}"] = torch.zeros(self.num_envs, dtype=torch.float, device=self.device)

        if self.rft.cfg.enabled:
            self._feet_contacts = RFTFeetContacts(
                self,
                self.rft,
                force_threshold=cfg.rft_contact_force_threshold,
                depth_threshold=cfg.rft_contact_depth_threshold,
                # same time window as the ContactSensor history
                history_length=round(
                    cfg.contact_sensor.history_length * max(cfg.contact_sensor.update_period, self.physics_dt)
                    / self.physics_dt
                ),
            )

    def _terrain_height_offset(self) -> torch.Tensor:
        rft = getattr(self, "rft", None)
        if rft is None or not rft.cfg.enabled:
            return self._zero_terrain_height_offset
        return rft.sand_height

    def _apply_action(self):
        super()._apply_action()  # joint targets, then the RFT wrench of this physics step
        self._feet_contacts.update(self.physics_dt)

    def _get_rewards(self) -> torch.Tensor:
        reward = super()._get_rewards()
        if not self._rft_reward_scales or self._rft() is None:
            return reward
        means = self.rft.terrain_means()
        for term, scale in self._rft_reward_scales.items():
            value = means[term].to(reward.dtype) * scale * self.step_dt
            reward = reward + value
            self.extras["reward_terms"][f"rft_{term}"] = value
            self._episode_sums[f"rft_{term}"] += value
        return reward
