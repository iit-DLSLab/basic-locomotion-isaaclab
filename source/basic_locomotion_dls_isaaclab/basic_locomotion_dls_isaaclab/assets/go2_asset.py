# Copyright (c) 2022-2024, The Berkeley Humanoid Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

import isaaclab.sim as sim_utils
from basic_locomotion_dls_isaaclab.actuators import IdentifiedActuatorElectricCfg
from isaaclab.assets.articulation import ArticulationCfg

from basic_locomotion_dls_isaaclab.assets import ISAAC_ASSET_DIR


# Aliengo robot configuration from mujoco
stiffness_mujoco = 25.0
damping_mujoco = 2.0

armature_mujoco = 0.01

friction_static_mujoco = 0.1# * 0.0
friction_dynamic_mujoco = 0.01# * 0.0
activation_vel = 0.01# * 0.0

static_friction_hip = 0.5 * 0.0
dynamic_friction_hip = 0.3 * 0.0
viscous_friction_hip = 0.3 * 0.0

static_friction_thigh = 0.5 * 0.0
dynamic_friction_thigh = 0.3 * 0.0
viscous_friction_thigh = 0.3 * 0.0

static_friction_calf = 0.5 * 0.0
dynamic_friction_calf = 0.3 * 0.0
viscous_friction_calf = 0.3 * 0.0

GO2_HIP_ACTUATOR_CFG = IdentifiedActuatorElectricCfg(
    joint_names_expr=[".*_hip_joint"],
    effort_limit=23.7,
    velocity_limit=30.1,
    saturation_effort=23.7,
    stiffness=stiffness_mujoco,
    damping=damping_mujoco,
    armature=armature_mujoco,
    friction_static=friction_static_mujoco,
    activation_vel=activation_vel,
    friction_dynamic=friction_dynamic_mujoco,

    friction = static_friction_hip,
    dynamic_friction = dynamic_friction_hip,
    viscous_friction = viscous_friction_hip,
)

GO2_THIGH_ACTUATOR_CFG = IdentifiedActuatorElectricCfg(
    joint_names_expr=[".*_thigh_joint"],
    effort_limit=23.7,
    velocity_limit=30.1,
    saturation_effort=23.7,
    stiffness=stiffness_mujoco,
    damping=damping_mujoco,
    armature=armature_mujoco,
    friction_static=friction_static_mujoco,
    activation_vel=activation_vel,
    friction_dynamic=friction_dynamic_mujoco,

    friction = static_friction_thigh,
    dynamic_friction = dynamic_friction_thigh,
    viscous_friction = viscous_friction_thigh,
)

GO2_CALF_ACTUATOR_CFG = IdentifiedActuatorElectricCfg(
    joint_names_expr=[".*_calf_joint"],
    effort_limit=45.43,
    velocity_limit=15.7,
    saturation_effort=45.43,
    stiffness=stiffness_mujoco,
    damping=damping_mujoco,
    armature=armature_mujoco,
    friction_static=friction_static_mujoco,
    activation_vel=activation_vel,
    friction_dynamic=friction_dynamic_mujoco,

    friction = static_friction_calf,
    dynamic_friction = dynamic_friction_calf,
    viscous_friction = viscous_friction_calf,
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
            enabled_self_collisions=False, solver_position_iteration_count=4, solver_velocity_iteration_count=0
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

    
    actuators={"hip": GO2_HIP_ACTUATOR_CFG, "thigh": GO2_THIGH_ACTUATOR_CFG,
               "calf": GO2_CALF_ACTUATOR_CFG},
    soft_joint_pos_limit_factor=0.95,
)
