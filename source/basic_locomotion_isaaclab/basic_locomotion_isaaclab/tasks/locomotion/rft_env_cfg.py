"""Configs of the locomotion tasks on granular terrain (sand), with the 3D-RFT foot contact of isaaclab-rft.

Each robot config gets:
- rft: the RFTCfg of the sand contact (one plane per foot from the foot height scanners the env already has);
- a 2.5 ms physics step, with the decimation raised to keep the policy rate (at 5 ms the RFT support is too soft and
  the foot force chatters);
- a Newton physics preset with one solver substep (Newton applies an external wrench only on the first substep).

The physics presets are new PresetCfg subclasses, not changed in __post_init__: the Isaac Lab hydra resolver reads the
preset alternatives from the class attributes.
"""

from __future__ import annotations

import copy

from isaaclab.utils.configclass import configclass

from isaaclab_rft.core.terrain_rewards import DIST_REWARD_SCALES
from isaaclab_rft.isaaclab.cfg import RFTCfg

from .aliengo_env_cfg import AliengoFlatEnvCfg, AliengoRoughBlindEnvCfg
from .aliengo_env_cfg import PhysicsCfg as AliengoPhysicsCfg
from .pegasus_env_cfg import PegasusFlatEnvCfg, PegasusRoughBlindEnvCfg
from .pegasus_env_cfg import PhysicsCfg as PegasusPhysicsCfg

FEET = ["FL_foot", "FR_foot", "RL_foot", "RR_foot"]
# The foot height scanners declared by LocomotionEnv._populate_scene_cfg, in foot order
FOOT_SCANNERS = [f"{foot.lower()}_height_scanner" for foot in FEET]

RFT_PHYSICS_DT = 1 / 400


def _sand_cfg() -> RFTCfg:
    # foot_radius is set from the robot config in _set_rft_sim
    return RFTCfg(
        foot_body_names=FEET,
        preset="slope",  # slope-aware 3D-RFT, calibrated against MPM simulations of Etna sand
        material="etna",
        sand_depth=0.15,  # sand surface above the rigid terrain [m]
        # probability that an env has sand, drawn at every reset; the others keep the rigid contact only
        sand_fraction=0.5,
        plane_source="foot_scanners",
        scanner_names=FOOT_SCANNERS,
        # weights in rft_terrain_reward_scales instead, so each term is its own reward term (see rft_env.py)
        terrain_reward_scales=None,
    )


def _one_substep(newton_cfg):
    """A copy of a NewtonCfg with one solver substep (NewtonCfg does not support replace())."""
    newton_cfg = copy.deepcopy(newton_cfg)
    newton_cfg.num_substeps = 1
    return newton_cfg


def _parent_post_init(cfg, cls) -> None:
    """Run the __post_init__ of the base robot config, if it has one."""
    post_init = getattr(super(cls, cfg), "__post_init__", None)
    if post_init is not None:
        post_init()


def _set_rft_sim(cfg, physics_cls) -> None:
    """RFT foot sphere from the robot config, 2.5 ms physics step at the same policy rate, Newton with one substep."""
    # The foot body is the center of the foot collision sphere (as in the rewards)
    cfg.rft.foot_radius = cfg.foot_radius
    policy_dt = cfg.sim.dt * cfg.decimation
    cfg.decimation = int(round(policy_dt / RFT_PHYSICS_DT))
    cfg.sim.dt = RFT_PHYSICS_DT
    cfg.sim.render_interval = cfg.decimation
    cfg.sim.physics = physics_cls()


@configclass
class _RFTEnvCfgMixin:
    # foot contact on sand: RFT force above this [N] or foot deeper than this below the sand surface [m]
    rft_contact_force_threshold = 1.0
    rft_contact_depth_threshold = 0.01
    # weights of the RFT terrain terms (slip, sinkage, bed_work, downslope_push), from rft_pegasus (Aliengo)
    rft_terrain_reward_scales = dict(DIST_REWARD_SCALES)


# ---------------------------------------------------------------------------------------------------- Pegasus
@configclass
class PegasusRFTPhysicsCfg(PegasusPhysicsCfg):
    newton_mjwarp = _one_substep(PegasusPhysicsCfg().newton_mjwarp)
    default = newton_mjwarp


@configclass
class PegasusFlatRFTEnvCfg(_RFTEnvCfgMixin, PegasusFlatEnvCfg):
    rft = _sand_cfg()

    def __post_init__(self):
        _parent_post_init(self, PegasusFlatRFTEnvCfg)
        _set_rft_sim(self, PegasusRFTPhysicsCfg)


@configclass
class PegasusRoughBlindRFTEnvCfg(_RFTEnvCfgMixin, PegasusRoughBlindEnvCfg):
    rft = _sand_cfg()

    def __post_init__(self):
        _parent_post_init(self, PegasusRoughBlindRFTEnvCfg)
        _set_rft_sim(self, PegasusRFTPhysicsCfg)


# ---------------------------------------------------------------------------------------------------- Aliengo
@configclass
class AliengoRFTPhysicsCfg(AliengoPhysicsCfg):
    newton_mjwarp = _one_substep(AliengoPhysicsCfg().newton_mjwarp)
    default = newton_mjwarp


@configclass
class AliengoFlatRFTEnvCfg(_RFTEnvCfgMixin, AliengoFlatEnvCfg):
    rft = _sand_cfg()

    def __post_init__(self):
        _parent_post_init(self, AliengoFlatRFTEnvCfg)
        _set_rft_sim(self, AliengoRFTPhysicsCfg)


@configclass
class AliengoRoughBlindRFTEnvCfg(_RFTEnvCfgMixin, AliengoRoughBlindEnvCfg):
    rft = _sand_cfg()

    def __post_init__(self):
        _parent_post_init(self, AliengoRoughBlindRFTEnvCfg)
        _set_rft_sim(self, AliengoRFTPhysicsCfg)
