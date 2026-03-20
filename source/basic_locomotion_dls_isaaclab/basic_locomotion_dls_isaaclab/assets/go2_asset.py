# Copyright (c) 2022-2024, The Berkeley Humanoid Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

import isaaclab.sim as sim_utils
from basic_locomotion_dls_isaaclab.actuators import IdentifiedActuatorElectricCfg, PaceDCMotorCfg
from isaaclab.assets.articulation import ArticulationCfg

from basic_locomotion_dls_isaaclab.assets import ISAAC_ASSET_DIR


GO2_HIP_ACTUATOR_CFG = PaceDCMotorCfg(
    joint_names_expr=[".*_hip_joint"],
    saturation_effort=23.7,
    effort_limit=23.7,
    velocity_limit=30.1,
    stiffness={".*": 20.0},  # P gain in Nm/rad
    damping={".*": 1.5},  # D gain in Nm s/rad
    encoder_bias={"FL_hip_joint": 0.1, "FR_hip_joint": 0.0065, "RL_hip_joint": 0.0451, "RR_hip_joint": -0.1000},  # encoder bias in radians
    # note: modeling coulomb friction if friction = dynamic_friction
    # > in newer Isaac Sim versions, friction is renamed to static_friction
    friction={"FL_hip_joint": 0.2840, "FR_hip_joint": 0.2236, "RL_hip_joint": 0.1627, "RR_hip_joint": 0.2284},  # static friction coefficient (Nm)
    dynamic_friction={"FL_hip_joint": 0.2840, "FR_hip_joint": 0.2236, "RL_hip_joint": 0.1627, "RR_hip_joint": 0.2284},  # dynamic friction coefficient (Nm)
    viscous_friction={"FL_hip_joint": 0.2274, "FR_hip_joint": 0.2544, "RL_hip_joint": 0.2424, "RR_hip_joint": 0.2727},  # viscous friction coefficient (Nm s/rad)
    armature={"FL_hip_joint": 0.0125, "FR_hip_joint": 0.0200, "RL_hip_joint": 0.0188, "RR_hip_joint": 0.0141},
    max_delay=2,  # max delay in simulation steps
)


GO2_THIGH_ACTUATOR_CFG = PaceDCMotorCfg(
    joint_names_expr=[".*_thigh_joint"],
    saturation_effort=23.7,
    effort_limit=23.7,
    velocity_limit=30.1,
    stiffness={".*": 20.0},  # P gain in Nm/rad
    damping={".*": 1.5},  # D gain in Nm s/rad
    encoder_bias={"FL_thigh_joint": 0.0931, "FR_thigh_joint": 0.0933, "RL_thigh_joint": 0.0998, "RR_thigh_joint": 0.0393},  # encoder bias in radians
    # note: modeling coulomb friction if friction = dynamic_friction
    # > in newer Isaac Sim versions, friction is renamed to static_friction
    friction={"FL_thigh_joint": 0.2167, "FR_thigh_joint": 0.1823, "RL_thigh_joint": 0.1621, "RR_thigh_joint": 0.2531},  # static friction coefficient (Nm)
    dynamic_friction={"FL_thigh_joint": 0.2167, "FR_thigh_joint": 0.1823, "RL_thigh_joint": 0.1621, "RR_thigh_joint": 0.2531},  # dynamic friction coefficient (Nm)
    viscous_friction={"FL_thigh_joint": 0.2427, "FR_thigh_joint": 0.2309, "RL_thigh_joint": 0.2409, "RR_thigh_joint": 0.2570},  # viscous friction coefficient (Nm s/rad)
    armature={"FL_thigh_joint": 0.0201, "FR_thigh_joint": 0.0200, "RL_thigh_joint": 0.0188, "RR_thigh_joint": 0.0141},
    max_delay=2,  # max delay in simulation steps
)


GO2_CALF_ACTUATOR_CFG = PaceDCMotorCfg(
    joint_names_expr=[".*_calf_joint"],
    saturation_effort=45.43,
    effort_limit=45.43,
    velocity_limit=15.7,
    stiffness={".*": 20.0},  # P gain in Nm/rad
    damping={".*": 1.5},  # D gain in Nm s/rad
    encoder_bias={"FL_calf_joint": 0.0999, "FR_calf_joint": 0.1000, "RL_calf_joint": 0.0959, "RR_calf_joint": 0.1000},  # encoder bias in radians
    # note: modeling coulomb friction if friction = dynamic_friction
    # > in newer Isaac Sim versions, friction is renamed to static_friction
    friction={"FL_calf_joint": 0.5000, "FR_calf_joint": 0.5000, "RL_calf_joint": 0.5000, "RR_calf_joint": 0.5000},  # static friction coefficient (Nm)
    dynamic_friction={"FL_calf_joint": 0.5000, "FR_calf_joint": 0.5000, "RL_calf_joint": 0.5000, "RR_calf_joint": 0.5000},  # dynamic friction coefficient (Nm)
    viscous_friction={"FL_calf_joint": 0.5195, "FR_calf_joint": 0.2717, "RL_calf_joint": 0.7357, "RR_calf_joint": 0.3621},  # viscous friction coefficient (Nm s/rad)
    armature={"FL_calf_joint": 0.0433, "FR_calf_joint": 0.0407, "RL_calf_joint": 0.0405, "RR_calf_joint": 0.0416},
    max_delay=2,  # max delay in simulation steps
)

GO2_CFG = ArticulationCfg(
    spawn=sim_utils.UsdFileCfg(
        usd_path=f"{ISAAC_ASSET_DIR}/go2_asset/from_xml/go2.usd",
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
            ".*L_hip_joint": 0.,
            ".*R_hip_joint": 0.,
            ".*_thigh_joint": 0.9,
            ".*_calf_joint": -1.8,
        },
        joint_vel={".*": 0.0},
    ),

    actuators={"hip": GO2_HIP_ACTUATOR_CFG, "thigh": GO2_THIGH_ACTUATOR_CFG, "calf": GO2_CALF_ACTUATOR_CFG},
    soft_joint_pos_limit_factor=0.95,
)
