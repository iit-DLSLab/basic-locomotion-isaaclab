# Copyright (c) 2022-2024, The Berkeley Humanoid Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

import isaaclab.sim as sim_utils
from basic_locomotion_isaaclab.actuators import IdentifiedActuatorElectricCfg, PaceDCMotorCfg
from isaaclab.assets.articulation import ArticulationCfg
from isaaclab.assets import AssetBaseCfg

from basic_locomotion_isaaclab.assets import ISAAC_ASSET_DIR

armature = [0.0017162850126624107, 0.013863112777471542, 0.015130503103137016, 0.002665896899998188, 0.013409794308245182, 0.015245151706039906, 0.003196015255525708, 0.013412774540483952, 0.014433911070227623, 0.0017740115290507674, 0.013637213036417961, 0.014545758254826069]
viscous_friction = [0.27535948157310486, 0.24064990878105164, 0.3018345534801483, 0.2694600224494934, 0.2563088536262512, 0.3042697310447693, 0.2853012979030609, 0.2598050534725189, 0.3056294918060303, 0.3122643232345581, 0.2689134478569031, 0.2910415828227997]
dynamic_friction = [0.4001328945159912, 0.33456742763519287, 0.4287477433681488, 0.4253632128238678, 0.3108210563659668, 0.31189993023872375, 0.3662518262863159, 0.2976449131965637, 0.3801218271255493, 0.6556040048599243, 0.32677721977233887, 0.564972460269928]
bias = [0.09997207671403885, 0.09998223930597305, 0.099995918571949, -0.09996622800827026, 0.09999663382768631, 0.09993762522935867, 0.09998243302106857, 0.09999308735132217, 0.09997328370809555, -0.09998500347137451, 0.09997231513261795, 0.09997696429491043]
delay = 2


ALIENGO_HIP_ACTUATOR_CFG = PaceDCMotorCfg(
    joint_names_expr=[".*_hip_joint"],
    saturation_effort=44.4,
    effort_limit=44.4,
    velocity_limit=21.0,
    stiffness={".*": 25.0},  # P gain in Nm/rad
    damping={".*": 2.0},  # D gain in Nm s/rad
    encoder_bias={"FL_hip_joint": bias[0], "FR_hip_joint": bias[3], "RL_hip_joint": bias[6], "RR_hip_joint": bias[9]},  # encoder bias in radians
    # note: modeling coulomb friction if friction = dynamic_friction
    # > in newer Isaac Sim versions, friction is renamed to static_friction
    friction={"FL_hip_joint": dynamic_friction[0], "FR_hip_joint": dynamic_friction[3], "RL_hip_joint": dynamic_friction[6], "RR_hip_joint": dynamic_friction[9]},  # static friction coefficient (Nm)
    dynamic_friction={"FL_hip_joint": dynamic_friction[0], "FR_hip_joint": dynamic_friction[3], "RL_hip_joint": dynamic_friction[6], "RR_hip_joint": dynamic_friction[9]},  # dynamic friction coefficient (Nm)
    viscous_friction={"FL_hip_joint": viscous_friction[0], "FR_hip_joint": viscous_friction[3], "RL_hip_joint": viscous_friction[6], "RR_hip_joint": viscous_friction[9]},  # viscous friction coefficient (Nm s/rad)
    armature={"FL_hip_joint": armature[0], "FR_hip_joint": armature[3], "RL_hip_joint": armature[6], "RR_hip_joint": armature[9]},
    max_delay=delay,  # max delay in simulation steps
)


ALIENGO_THIGH_ACTUATOR_CFG = PaceDCMotorCfg(
    joint_names_expr=[".*_thigh_joint"],
    saturation_effort=44.4,
    effort_limit=44.4,
    velocity_limit=21.0,
    stiffness={".*": 25.0},  # P gain in Nm/rad
    damping={".*": 2.0},  # D gain in Nm s/rad
    encoder_bias={"FL_thigh_joint": bias[1], "FR_thigh_joint": bias[4], "RL_thigh_joint": bias[7], "RR_thigh_joint": bias[10]},  # encoder bias in radians
    # note: modeling coulomb friction if friction = dynamic_friction
    # > in newer Isaac Sim versions, friction is renamed to static_friction
    friction={"FL_thigh_joint": dynamic_friction[1], "FR_thigh_joint": dynamic_friction[4], "RL_thigh_joint": dynamic_friction[7], "RR_thigh_joint": dynamic_friction[10]},  # static friction coefficient (Nm)
    dynamic_friction={"FL_thigh_joint": dynamic_friction[1], "FR_thigh_joint": dynamic_friction[4], "RL_thigh_joint": dynamic_friction[7], "RR_thigh_joint": dynamic_friction[10]},  # dynamic friction coefficient (Nm)
    viscous_friction={"FL_thigh_joint": viscous_friction[1], "FR_thigh_joint": viscous_friction[4], "RL_thigh_joint": viscous_friction[7], "RR_thigh_joint": viscous_friction[10]},  # viscous friction coefficient (Nm s/rad)
    armature={"FL_thigh_joint":armature[1], "FR_thigh_joint": armature[4], "RL_thigh_joint": armature[7], "RR_thigh_joint": armature[10]},
    max_delay=delay,  # max delay in simulation steps
)


ALIENGO_CALF_ACTUATOR_CFG = PaceDCMotorCfg(
    joint_names_expr=[".*_calf_joint"],
    saturation_effort=44.4,
    effort_limit=44.4,
    velocity_limit=21.0,
    stiffness={".*": 25.0},  # P gain in Nm/rad
    damping={".*": 2.0},  # D gain in Nm s/rad
    encoder_bias={"FL_calf_joint": bias[2], "FR_calf_joint": bias[5], "RL_calf_joint": bias[8], "RR_calf_joint": bias[11]},  # encoder bias in radians
    # note: modeling coulomb friction if friction = dynamic_friction
    # > in newer Isaac Sim versions, friction is renamed to static_friction
    friction={"FL_calf_joint": dynamic_friction[2], "FR_calf_joint": dynamic_friction[5], "RL_calf_joint": dynamic_friction[8], "RR_calf_joint": dynamic_friction[11]},  # static friction coefficient (Nm)
    dynamic_friction={"FL_calf_joint": dynamic_friction[2], "FR_calf_joint": dynamic_friction[5], "RL_calf_joint": dynamic_friction[8], "RR_calf_joint": dynamic_friction[11]},  # dynamic friction coefficient (Nm)
    viscous_friction={"FL_calf_joint": viscous_friction[2], "FR_calf_joint": viscous_friction[5], "RL_calf_joint": viscous_friction[8], "RR_calf_joint": viscous_friction[11]},  # viscous friction coefficient (Nm s/rad)
    armature={"FL_calf_joint": armature[2], "FR_calf_joint": armature[5], "RL_calf_joint": armature[8], "RR_calf_joint": armature[11]},
    max_delay=delay,  # max delay in simulation steps
)


ALIENGO_CFG = ArticulationCfg(
    prim_path=None,
    spawn=sim_utils.UsdFileCfg(
        usd_path=f"{ISAAC_ASSET_DIR}/../../../../robot_model/aliengo/aliengo.usd",
        activate_contact_sensors=True,
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=False,
            retain_accelerations=False,
            linear_damping=0.0,
            angular_damping=0.0,
            max_linear_velocity=1000.0,
            max_angular_velocity=1000.0,
            max_depenetration_velocity=1.0,
        ),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=True, solver_position_iteration_count=4, solver_velocity_iteration_count=0
        ),
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        pos=(0.0, 0.0, 0.4),
        joint_pos={
            ".*L_hip_joint": 0.0,
            ".*R_hip_joint": 0.0,
            ".*_thigh_joint": 0.9,
            ".*_calf_joint": -1.8,
        },
        joint_vel={".*": 0.0},
    ),

    actuators={"hip": ALIENGO_HIP_ACTUATOR_CFG, "thigh": ALIENGO_THIGH_ACTUATOR_CFG, "calf": ALIENGO_CALF_ACTUATOR_CFG},
    soft_joint_pos_limit_factor=0.95,
)


CAMERA_USD_CFG = AssetBaseCfg(
    prim_path="/World/envs/env_.*/Robot/base/d435",
    spawn=sim_utils.UsdFileCfg(usd_path=f"{ISAAC_ASSET_DIR}/d435.usd",),
    init_state=AssetBaseCfg.InitialStateCfg(
            pos=(0.33, 0.0, 0.08), 
            rot=(-0.405579, 0.579228, -0.579228, 0.405579)
    )
)
