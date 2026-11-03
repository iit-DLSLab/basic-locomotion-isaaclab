# Copyright (c) 2022-2024, The Berkeley Humanoid Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

import isaaclab.sim as sim_utils
from basic_locomotion_isaaclab.actuators import IdentifiedActuatorElectricCfg, PaceDCMotorCfg
from isaaclab.assets.articulation import ArticulationCfg

from basic_locomotion_isaaclab.assets import ISAAC_ASSET_DIR

# Order: FL_hip, FL_thigh, FL_calf, FR_hip, FR_thigh, FR_calf, RL_hip, RL_thigh, RL_calf, RR_hip, RR_thigh, RR_calf
armature = [0.015399526804685593, 0.02050127647817135, 0.037081241607666016, 0.018103286623954773, 0.019743947312235832, 0.03752225264906883, 0.017827438190579414, 0.01892966590821743, 0.03460302576422691, 0.01647171564400196, 0.018195493146777153, 0.03529830649495125]
viscous_friction = [0.19811680912971497, 0.259413480758667, 0.23080530762672424, 0.2374870777130127, 0.23283368349075317, 0.22543010115623474, 0.2243238091468811, 0.24681055545806885, 0.13911908864974976, 0.222743958234787, 0.2360401153564453, 0.20377448201179504]
dynamic_friction = [0.29993337392807007, 0.22318589687347412, 0.6745705008506775, 0.25826162099838257, 0.2497260570526123, 0.507129430770874, 0.17222875356674194, 0.20518887042999268, 1.1109280586242676, 0.23757243156433105, 0.22198569774627686, 0.49201714992523193]
bias = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
delay = 1

Kp = 25.0
Kd = 1.5

GO2_HIP_ACTUATOR_CFG = PaceDCMotorCfg(
    joint_names_expr=[".*_hip_joint"],
    saturation_effort=23.7,
    effort_limit=23.7,
    velocity_limit=30.1,
    stiffness={".*": Kp},  # P gain in Nm/rad
    damping={".*": Kd},  # D gain in Nm s/rad
    encoder_bias={"FL_hip_joint": bias[0], "FR_hip_joint": bias[3], "RL_hip_joint": bias[6], "RR_hip_joint": bias[9]},  # encoder bias in radians
    # note: modeling coulomb friction if friction = dynamic_friction
    # > in newer Isaac Sim versions, friction is renamed to static_friction
    friction={"FL_hip_joint": dynamic_friction[0], "FR_hip_joint": dynamic_friction[3], "RL_hip_joint": dynamic_friction[6], "RR_hip_joint": dynamic_friction[9]},  # static friction coefficient (Nm)
    dynamic_friction={"FL_hip_joint": dynamic_friction[0], "FR_hip_joint": dynamic_friction[3], "RL_hip_joint": dynamic_friction[6], "RR_hip_joint": dynamic_friction[9]},  # dynamic friction coefficient (Nm)
    viscous_friction={"FL_hip_joint": viscous_friction[0], "FR_hip_joint": viscous_friction[3], "RL_hip_joint": viscous_friction[6], "RR_hip_joint": viscous_friction[9]},  # viscous friction coefficient (Nm s/rad)
    armature={"FL_hip_joint": armature[0], "FR_hip_joint": armature[3], "RL_hip_joint": armature[6], "RR_hip_joint": armature[9]},
    max_delay=delay,  # max delay in simulation steps
)


GO2_THIGH_ACTUATOR_CFG = PaceDCMotorCfg(
    joint_names_expr=[".*_thigh_joint"],
    saturation_effort=23.7,
    effort_limit=23.7,
    velocity_limit=30.1,
    stiffness={".*": Kp},  # P gain in Nm/rad
    damping={".*": Kd},  # D gain in Nm s/rad
    encoder_bias={"FL_thigh_joint": bias[1], "FR_thigh_joint": bias[4], "RL_thigh_joint": bias[7], "RR_thigh_joint": bias[10]},  # encoder bias in radians
    # note: modeling coulomb friction if friction = dynamic_friction
    # > in newer Isaac Sim versions, friction is renamed to static_friction
    friction={"FL_thigh_joint": dynamic_friction[1], "FR_thigh_joint": dynamic_friction[4], "RL_thigh_joint": dynamic_friction[7], "RR_thigh_joint": dynamic_friction[10]},  # static friction coefficient (Nm)
    dynamic_friction={"FL_thigh_joint": dynamic_friction[1], "FR_thigh_joint": dynamic_friction[4], "RL_thigh_joint": dynamic_friction[7], "RR_thigh_joint": dynamic_friction[10]},  # dynamic friction coefficient (Nm)
    viscous_friction={"FL_thigh_joint": viscous_friction[1], "FR_thigh_joint": viscous_friction[4], "RL_thigh_joint": viscous_friction[7], "RR_thigh_joint": viscous_friction[10]},  # viscous friction coefficient (Nm s/rad)
    armature={"FL_thigh_joint":armature[1], "FR_thigh_joint": armature[4], "RL_thigh_joint": armature[7], "RR_thigh_joint": armature[10]},
    max_delay=delay,  # max delay in simulation steps
)


GO2_CALF_ACTUATOR_CFG = PaceDCMotorCfg(
    joint_names_expr=[".*_calf_joint"],
    saturation_effort=45.43,
    effort_limit=45.43,
    velocity_limit=15.7,
    stiffness={".*": Kp},  # P gain in Nm/rad
    damping={".*": Kd},  # D gain in Nm s/rad
    encoder_bias={"FL_calf_joint": bias[2], "FR_calf_joint": bias[5], "RL_calf_joint": bias[8], "RR_calf_joint": bias[11]},  # encoder bias in radians
    # note: modeling coulomb friction if friction = dynamic_friction
    # > in newer Isaac Sim versions, friction is renamed to static_friction
    friction={"FL_calf_joint": dynamic_friction[2], "FR_calf_joint": dynamic_friction[5], "RL_calf_joint": dynamic_friction[8], "RR_calf_joint": dynamic_friction[11]},  # static friction coefficient (Nm)
    dynamic_friction={"FL_calf_joint": dynamic_friction[2], "FR_calf_joint": dynamic_friction[5], "RL_calf_joint": dynamic_friction[8], "RR_calf_joint": dynamic_friction[11]},  # dynamic friction coefficient (Nm)
    viscous_friction={"FL_calf_joint": viscous_friction[2], "FR_calf_joint": viscous_friction[5], "RL_calf_joint": viscous_friction[8], "RR_calf_joint": viscous_friction[11]},  # viscous friction coefficient (Nm s/rad)
    armature={"FL_calf_joint": armature[2], "FR_calf_joint": armature[5], "RL_calf_joint": armature[8], "RR_calf_joint": armature[11]},
    max_delay=delay,  # max delay in simulation steps
)

GO2_CFG = ArticulationCfg(
    spawn=sim_utils.UsdFileCfg(
        usd_path=f"{ISAAC_ASSET_DIR}/../../../../robot_model/go2/generated_usd/go2.usda",
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
