# Copyright (c) 2022-2024, The Isaac Lab Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

from __future__ import annotations

import gymnasium as gym
import math
import torch

import isaaclab.envs.mdp as mdp
import isaaclab.sim as sim_utils
import isaaclab.utils.math as math_utils
from isaaclab.assets import Articulation, ArticulationCfg, AssetBaseCfg
from isaaclab.envs import DirectRLEnv, DirectRLEnvCfg
from isaaclab.managers import EventTermCfg as EventTerm
from isaaclab.scene import InteractiveSceneCfg
from isaaclab.sensors import (
    ContactSensor,
    ContactSensorCfg,
    Imu,
    MultiMeshRayCaster,
    MultiMeshRayCasterCamera,
    MultiMeshRayCasterCameraCfg,
    RayCaster,
    RayCasterCamera,
    RayCasterCameraCfg,
    RayCasterCfg,
    TiledCamera,
    TiledCameraCfg,
    patterns,
)
from isaaclab.sim import SimulationCfg
from isaaclab.terrains import TerrainImporterCfg
from isaaclab.utils import configclass


from .aliengo_env_cfg import AliengoFlatEnvCfg, AliengoRoughBlindEnvCfg, AliengoRoughVisionEnvCfg
from .go2_env_cfg import Go2FlatEnvCfg, Go2RoughVisionEnvCfg, Go2RoughBlindEnvCfg
from .hyqreal_env_cfg import HyQRealFlatEnvCfg, HyQRealRoughVisionEnvCfg, HyQRealRoughBlindEnvCfg
from .b2_env_cfg import B2FlatEnvCfg, B2RoughVisionEnvCfg, B2RoughBlindEnvCfg
from .pegasus_env_cfg import PegasusFlatEnvCfg, PegasusRoughVisionEnvCfg, PegasusRoughBlindEnvCfg

from basic_locomotion_isaaclab.tasks import custom_observations, custom_rewards, custom_events
from basic_locomotion_isaaclab.tasks.supervised_learning_networks import FrozenRandomMlpEncoder, create_supervised_network

class LocomotionEnv(DirectRLEnv):

    def __init__(self, cfg, render_mode: str | None = None, **kwargs):
        self._edge_map_visualizer = None
        self._configure_scene(cfg)
        super().__init__(cfg, render_mode, **kwargs)

        # Explicit controllers own PD gains; PhysX drive gains are zero for these joints.
        self._nominal_actuator_stiffness = {
            name: actuator.stiffness.clone() for name, actuator in self._robot.actuators.items()
        }
        self._nominal_actuator_damping = {
            name: actuator.damping.clone() for name, actuator in self._robot.actuators.items()
        }

        # Joint position command (deviation from default joint positions)
        self._actions = torch.zeros(self.num_envs, gym.spaces.flatdim(self.single_action_space), device=self.device)
        self._previous_actions = torch.zeros(
            self.num_envs, gym.spaces.flatdim(self.single_action_space), device=self.device
        )
        self._previous_previous_actions = torch.zeros(
            self.num_envs, gym.spaces.flatdim(self.single_action_space), device=self.device
        )

        # X/Y linear velocity and yaw angular velocity commands
        self._commands = torch.zeros(self.num_envs, 3, device=self.device)

        # Swing peak
        self._swing_peak = torch.tensor([0.0, 0.0, 0.0, 0.0], device=self.device).repeat(self.num_envs,1)
        self._swing_peak_periodic = torch.tensor([0.0, 0.0, 0.0, 0.0], device=self.device).repeat(self.num_envs,1)
        
        # Desired Hip Offset
        self._desired_hip_offset = torch.tensor([-self.cfg.desired_hip_offset, self.cfg.desired_hip_offset, -self.cfg.desired_hip_offset, self.cfg.desired_hip_offset], device=self.device)
        
        # Periodic gait
        self._step_freq = torch.tensor(self.cfg.desired_step_freq, device=self.device)
        self._duty_factor = torch.tensor(self.cfg.desired_duty_factor, device=self.device)
        self._phase_offset = torch.tensor(self.cfg.desired_phase_offset, device=self.device).repeat(self.num_envs,1)
        self._phase_signal = self._phase_offset.clone()# + self.step_dt * self._step_freq * torch.rand(self.num_envs, 1, device=self.device)*10.
        self._phase_signal = self._phase_signal % 1.0


        # Observation history
        self._observation_history = torch.zeros(self.num_envs, cfg.history_length, cfg.single_observation_space, device=self.device)

        # RMA
        if(cfg.use_rma == True):
            self._rma_network = create_supervised_network(
                cfg.rma_observation_space,
                cfg.rma_output_space,
                network_type=getattr(cfg, "rma_network_type", "mlp"),
                sequence_length=cfg.rma_history_length,
            )
            self._rma_network.to(self.device)
            
            if self.cfg.rma_use_latent_space:
                self._rma_latent_encoder = FrozenRandomMlpEncoder(
                    cfg.rma_privileged_observation_space,
                    cfg.rma_output_space,
                    hidden_features=getattr(cfg, "rma_latent_encoder_hidden_features", 128),
                    seed=getattr(cfg, "rma_latent_encoder_seed", 0),
                )
                self._rma_latent_encoder.to(self.device)
            self._observation_history_rma = torch.zeros(self.num_envs, cfg.rma_history_length, cfg.single_rma_observation_space, device=self.device)
            if self.cfg.observation_noise_model:
                self._observation_noise_model_rma: NoiseModel = self.cfg.observation_noise_model.class_type(
                    self.cfg.observation_noise_model, num_envs=self.num_envs, device=self.device
                )

        # Learned State Estimator
        if(cfg.use_concurrent_state_est == True):
            self._concurrent_state_est_network = create_supervised_network(
                cfg.concurrent_state_est_observation_space,
                cfg.concurrent_state_est_output_space,
                network_type=getattr(cfg, "concurrent_state_est_network_type", "mlp"),
                sequence_length=cfg.concurrent_state_est_history_length,
            )
            self._concurrent_state_est_network.to(self.device)
            self._observation_history_concurrent_state_est = torch.zeros(self.num_envs, cfg.concurrent_state_est_history_length, cfg.single_concurrent_state_est_observation_space, device=self.device)
            if self.cfg.observation_noise_model:
                self._observation_noise_model_concurrent_state_est: NoiseModel = self.cfg.observation_noise_model.class_type(
                    self.cfg.observation_noise_model, num_envs=self.num_envs, device=self.device
                )

        # Logging
        self._episode_sums = {
            key: torch.zeros(self.num_envs, dtype=torch.float, device=self.device)
            for key in [
                "track_height_exp",
                "track_lin_vel_xy_exp",
                "track_lin_vel_z_l2",
                "track_orientation_l2",
                "track_ang_vel_xy_l2",
                "track_ang_vel_z_exp",

                "undesired_contacts",
                "action_rate_l2",
                "action_smoothness_l2",
                
                "joints_hip_pos_l2",
                "joints_thigh_pos_l2",
                "joints_calf_pos_l2",
                "joints_acc_l2",
                "joints_torques_l2",
                "joints_energy_l1",
                
                "feet_air_time",
                "feet_air_time_variance",

                "feet_height_clearance_periodic",
                "feet_height_clearance_aperiodic",
                "feet_height_clearance_mujoco_periodic",
                "feet_height_clearance_mujoco_aperiodic",
                "feet_slide",
                "feet_to_hip_distance_l2",
                "feet_edge",
                "feet_vertical_surface_contacts",

                "periodic_contact_suggestion",
                "stance_contact_suggestion",
            ]
        }
        # Get specific body indices
        self._base_contact_sensor_id, _ = self._contact_sensor.find_bodies("base")
        self._feet_contact_sensor_ids, _ = self._contact_sensor.find_bodies(["FL_foot", "FR_foot", "RL_foot", "RR_foot"], preserve_order=True)
        self._hip_contact_sensor_ids, _ = self._contact_sensor.find_bodies(["FL_hip", "FR_hip", "RL_hip", "RR_hip"], preserve_order=True)
        self._thigh_contact_sensor_ids, _ = self._contact_sensor.find_bodies(["FL_thigh", "FR_thigh", "RL_thigh", "RR_thigh"], preserve_order=True)
        self._undesired_contact_body_ids = self._base_contact_sensor_id + self._hip_contact_sensor_ids + self._thigh_contact_sensor_ids

        
        self._feet_ids_robot, _ = self._robot.find_bodies(["FL_foot", "FR_foot", "RL_foot", "RR_foot"], preserve_order=True)
        self._hip_ids_robot, _ = self._robot.find_bodies(["FL_hip", "FR_hip", "RL_hip", "RR_hip"], preserve_order=True)

        # Ensure the order is consistent with the one expected in the cfg
        self._ids_joints_order = self._robot.find_joints(name_keys=self.cfg.desired_joints_order, preserve_order=True)[0]

        if getattr(self.cfg, "visualize_edge_map", False):
            self.set_debug_vis(True)


    @staticmethod
    def _configure_scene(cfg):
        """Declare scene entities before Isaac Lab builds and clones the scene."""
        cfg.scene.robot = cfg.robot
        cfg.scene.contact_sensor = cfg.contact_sensor
        cfg.scene.pose_height_scanner = cfg.pose_height_scanner
        for foot_name in ("FL_foot", "FR_foot", "RL_foot", "RR_foot"):
            setattr(cfg.scene, f"{foot_name.lower()}_height_scanner", cfg.foot_height_scanner.replace(
                prim_path=f"{{ENV_REGEX_NS}}/Robot/{foot_name}",
                visualizer_cfg=cfg.foot_height_scanner.visualizer_cfg.replace(
                    prim_path=f"/Visuals/{foot_name}HeightScanner"
                ),
            ))
        if getattr(cfg, "use_vision", False):
            cfg.scene.perceptive_height_scanner = cfg.perceptive_height_scanner
            cfg.scene.edge_height_scanner = cfg.edge_height_scanner
        if getattr(cfg, "use_depth_camera", False):
            cfg.scene.depth_camera = cfg.depth_camera
        if getattr(cfg, "use_unitree_l2_lidar", False):
            cfg.scene.unitree_l2_lidar = cfg.unitree_l2_lidar
        cfg.scene.imu = cfg.imu
        cfg.scene.terrain = cfg.terrain
        cfg.scene.light = AssetBaseCfg(
            prim_path="/World/Light",
            spawn=sim_utils.DomeLightCfg(intensity=2000.0, color=(0.75, 0.75, 0.75)),
        )

    def _setup_scene(self):
        self._robot = self.scene["robot"]
        self._contact_sensor = self.scene["contact_sensor"]
        self._pose_height_scanner = self.scene["pose_height_scanner"]
        self._foot_height_scanners = [
            self.scene[f"{name}_height_scanner"] for name in ("fl_foot", "fr_foot", "rl_foot", "rr_foot")
        ]
        if getattr(self.cfg, "use_vision", False):
            self._perceptive_height_scanner = self.scene["perceptive_height_scanner"]
            self._edge_height_scanner = self.scene["edge_height_scanner"]
        if getattr(self.cfg, "use_depth_camera", False):
            self._depth_camera = self.scene["depth_camera"]
        if getattr(self.cfg, "use_unitree_l2_lidar", False):
            self._unitree_l2_lidar = self.scene["unitree_l2_lidar"]
        self._imu = self.scene["imu"]
        self._terrain = self.scene.terrain


    def _pre_physics_step(self, actions: torch.Tensor):
        self._previous_previous_actions = self._previous_actions.clone()
        self._previous_actions = self._actions.clone()
        self._actions = actions.clone()
        default_joint_pos_ordered = self._robot.data.default_joint_pos.torch[:, self._ids_joints_order]
        
        # Clip the action
        self._actions = torch.clamp(self._actions, -self.cfg.desired_clip_actions, self.cfg.desired_clip_actions)

        # Filter the action
        if(self.cfg.use_filter_actions):
            alpha = 0.8
            temp = alpha * self._actions + (1 - alpha) * self._previous_actions
            self._processed_actions = self.cfg.action_scale * temp + default_joint_pos_ordered
        else:
            self._processed_actions = self.cfg.action_scale * self._actions + default_joint_pos_ordered


    def _apply_action(self):
        self._robot.set_joint_position_target(self._processed_actions, joint_ids=self._ids_joints_order)


    def _get_observations(self) -> dict:
        
        # Sample new commands if needed
        custom_events._get_new_random_commands(self)


        # Observation --------------------------------------------------------------------------------------
        clock_data = None
        if(self.cfg.use_clock_signal):
            self._phase_signal += self.step_dt * self._step_freq
            self._phase_signal = self._phase_signal % 1.0
            clock_data = torch.vstack([self._phase_signal[:,0], self._phase_signal[:,1], self._phase_signal[:,2], self._phase_signal[:,3]]).T
            # all the envs that are not moving, we put -1
            should_move = torch.norm(self._commands[:, :3], dim=1) > 0.01
            clock_data[:, :] = clock_data[:, :]*should_move.unsqueeze(1).expand(-1, 4) + -1.0* ~should_move.unsqueeze(1).expand(-1, 4)
            

        # Choosing the main source of observation
        if(self.cfg.use_concurrent_state_est):
            # If concurrent SE/Learned State Estimator, we predict linear and angular vel from IMU
            base_linear = custom_observations._get_concurrent_state_estimation(self)
            base_ang_vel = self._imu.data.ang_vel_b.torch
            projected_gravity_b = self._imu.data.projected_gravity_b.torch
        elif(self.cfg.use_imu):
            # Using directly the IMU
            base_linear = self._imu.data.lin_acc_b.torch
            base_ang_vel = self._imu.data.ang_vel_b.torch
            projected_gravity_b = self._imu.data.projected_gravity_b.torch
        else:
            #Using a model-based state estimation
            base_linear = self._robot.data.root_lin_vel_b.torch
            base_ang_vel = self._robot.data.root_ang_vel_b.torch
            projected_gravity_b = self._robot.data.projected_gravity_b.torch
        
        
        # Standard Obs for the Actor/Critic
        obs = torch.cat(
            [
                tensor
                for tensor in (
                    base_linear,
                    base_ang_vel,
                    projected_gravity_b,
                    self._commands,
                    self._robot.data.joint_pos.torch[:, self._ids_joints_order] - self._robot.data.default_joint_pos.torch[:, self._ids_joints_order],
                    self._robot.data.joint_vel.torch[:, self._ids_joints_order],
                    self._actions,
                    clock_data,
                )
                if tensor is not None
            ],
            dim=-1,
        )
        if(self.cfg.use_observation_history):
            #the bottom element is the newest observation!!
            self._observation_history = torch.cat((self._observation_history[:,1:,:], obs.unsqueeze(1)), dim=1)
            obs = torch.flatten(self._observation_history, start_dim=1)


        observations = {"common": obs}


        # Add heightmap data to obs if needed
        if(getattr(self.cfg, "use_vision", False)):
            height_data = (
                self._perceptive_height_scanner.data.pos_w.torch[:, 2].unsqueeze(1)
                - self._perceptive_height_scanner.data.ray_hits_w.torch[..., 2]
                - 0.5
            )
            height_data = torch.nan_to_num(height_data, nan=0.0, posinf=1.0, neginf=-1.0)
            height_data = height_data.clip(-1.0, 1.0)
            obs = torch.cat((obs, height_data), dim=-1)   


        # Critic OBS could be different if needed
        if(self.cfg.use_asymmetric_ppo):
            obs_critic = custom_observations._get_privileged_observation_asymmetric(self)
            observations["critic"] = torch.cat((obs, obs_critic), dim=-1)
        else:
            observations["critic"] = obs


        # If RMA, we add some other predicted obs AFTER the critic asymmetric obs to avoid duplication
        if(self.cfg.use_rma):
            # Predict the RMA observation
            obs_rma = custom_observations._get_rma(self)
            obs = torch.cat((obs, obs_rma), dim=-1)


        # Actor OBS - here after the critic to avoid duplication with rma obs
        # if asymmetric ppo is used
        observations["policy"] = obs    
        # ------------------------------------------------------------------------------------------

        # AMP related observation if used
        if(self.cfg.use_amp):
            obs_amp = torch.cat(
                [
                    tensor
                    for tensor in (
                        #self._robot.data.root_quat_w.torch,
                        self._robot.data.joint_pos.torch[:, self._ids_joints_order],
                        self._robot.data.joint_vel.torch[:, self._ids_joints_order],
                        self._robot.data.root_lin_vel_b.torch,
                        self._robot.data.root_ang_vel_b.torch,
                    )
                    if tensor is not None
                ],
                dim=-1,
            )
            observations["amp"] = obs_amp

        # --------------------------------------------------------------------------------------------
        return observations


    def _get_rewards(self) -> torch.Tensor:

        track_height_exp = custom_rewards.track_height_exp(self)
        track_lin_vel_xy_exp = custom_rewards.track_lin_vel_xy_exp(self)
        track_lin_vel_z_l2 = custom_rewards.track_lin_vel_z_l2(self)
        track_orientation_l2 = custom_rewards.track_orientation_l2(self)
        track_ang_vel_xy_l2 = custom_rewards.track_ang_vel_xy_l2(self)
        track_ang_vel_z_exp = custom_rewards.track_ang_vel_z_exp(self)

        undesired_contacts = custom_rewards.undesired_contacts(self)
        action_rate_l2 = custom_rewards.action_rate_l2(self)
        action_smoothness_l2 = custom_rewards.action_smoothness_l2(self)

        joints_hip_pos_l2 = custom_rewards.joints_hip_pos_l2(self)
        joints_thigh_pos_l2 = custom_rewards.joints_thigh_pos_l2(self)
        joints_calf_pos_l2 = custom_rewards.joints_calf_pos_l2(self)
        joints_acc_l2 = custom_rewards.joints_acc_l2(self)
        joints_torques_l2 = custom_rewards.joints_torques_l2(self)
        joints_energy_l1 = custom_rewards.joints_energy_l1(self)

        feet_air_time = custom_rewards.feet_air_time(self)
        feet_air_time_variance = custom_rewards.feet_air_time_variance(self)

        feet_slide = custom_rewards.feet_slide(self)
        feet_edge = custom_rewards.feet_edge(self)
        periodic_contact_suggestion = custom_rewards.periodic_contact_suggestion(self)
        stance_contact_suggestion = custom_rewards.stance_contact_suggestion(self)
        feet_height_clearance_mujoco_aperiodic = custom_rewards.feet_height_clearance_mujoco_aperiodic(self)
        feet_height_clearance_mujoco_periodic = custom_rewards.feet_height_clearance_mujoco_periodic(self)
        feet_height_clearance_periodic = custom_rewards.feet_height_clearance_periodic(self)
        feet_height_clearance_aperiodic = custom_rewards.feet_height_clearance_aperiodic(self)
        feet_to_hip_distance_l2 = custom_rewards.feet_to_hip_distance_l2(self)
        feet_vertical_surface_contacts = custom_rewards.feet_vertical_surface_contacts(self)

        rewards = {
            "track_height_exp": track_height_exp * self.cfg.height_reward_scale * self.step_dt,
            "track_lin_vel_xy_exp": track_lin_vel_xy_exp * self.cfg.lin_vel_reward_scale * self.step_dt,
            "track_lin_vel_z_l2": track_lin_vel_z_l2 * self.cfg.z_vel_reward_scale * self.step_dt,
            "track_orientation_l2": track_orientation_l2 * self.cfg.orientation_reward_scale * self.step_dt,
            "track_ang_vel_xy_l2": track_ang_vel_xy_l2 * self.cfg.ang_vel_reward_scale * self.step_dt,
            "track_ang_vel_z_exp": track_ang_vel_z_exp * self.cfg.yaw_rate_reward_scale * self.step_dt,

            "undesired_contacts": undesired_contacts * self.cfg.undersired_contact_reward_scale * self.step_dt,
            "action_rate_l2": action_rate_l2 * self.cfg.action_rate_reward_scale * self.step_dt,
            "action_smoothness_l2": action_smoothness_l2 * self.cfg.action_smoothness_reward_scale * self.step_dt,

            "joints_hip_pos_l2": joints_hip_pos_l2 * self.cfg.joints_hip_position_reward_scale * self.step_dt,
            "joints_thigh_pos_l2": joints_thigh_pos_l2 * self.cfg.joints_thigh_position_reward_scale * self.step_dt,
            "joints_calf_pos_l2": joints_calf_pos_l2 * self.cfg.joints_calf_position_reward_scale * self.step_dt,
            "joints_acc_l2": joints_acc_l2 * self.cfg.joints_accel_reward_scale * self.step_dt,
            "joints_torques_l2": joints_torques_l2 * self.cfg.joints_torque_reward_scale * self.step_dt,
            "joints_energy_l1": joints_energy_l1 * self.cfg.joints_energy_reward_scale * self.step_dt,

            "feet_air_time": feet_air_time * self.cfg.feet_air_time_reward_scale * self.step_dt,
            "feet_air_time_variance": feet_air_time_variance * self.cfg.feet_air_time_variance_reward_scale * self.step_dt,
            
            "feet_height_clearance_aperiodic": feet_height_clearance_aperiodic * self.cfg.feet_height_clearance_aperiodic_reward_scale * self.step_dt,
            "feet_height_clearance_periodic": feet_height_clearance_periodic * self.cfg.feet_height_clearance_periodic_reward_scale * self.step_dt,
            "feet_height_clearance_mujoco_aperiodic": feet_height_clearance_mujoco_aperiodic * self.cfg.feet_height_clearance_mujoco_aperiodic_reward_scale * self.step_dt,
            "feet_height_clearance_mujoco_periodic": feet_height_clearance_mujoco_periodic * self.cfg.feet_height_clearance_mujoco_periodic_reward_scale * self.step_dt,
            
            "feet_slide": feet_slide * self.cfg.feet_slide_reward_scale * self.step_dt,
            "feet_to_hip_distance_l2": feet_to_hip_distance_l2 * self.cfg.feet_to_hip_distance_reward_scale * self.step_dt,
            "feet_edge": feet_edge * self.cfg.feet_edge_reward_scale * self.step_dt,
            "feet_vertical_surface_contacts": feet_vertical_surface_contacts * self.cfg.feet_vertical_surface_contacts_reward_scale * self.step_dt,

            "periodic_contact_suggestion": periodic_contact_suggestion * self.cfg.periodic_contact_suggestion_reward_scale * self.step_dt,
            "stance_contact_suggestion": stance_contact_suggestion * self.cfg.stance_contact_suggestion_reward_scale * self.step_dt,
            
        }
        reward = torch.sum(torch.stack(list(rewards.values())), dim=0)

        # Check for NaNs and Infs
        if torch.isnan(reward).any() or torch.isinf(reward).any():
            print("NaN or Inf detected in reward computation. Setting reward to zero for affected environments.")
            breakpoint()  # For debugging purposes
            reward = torch.where(torch.isnan(reward) | torch.isinf(reward), torch.zeros_like(reward), reward)
        
        # Logging
        for key, value in rewards.items():
            self._episode_sums[key] += value
        return reward


    def _get_dones(self) -> tuple[torch.Tensor, torch.Tensor]:
        time_out = self.episode_length_buf >= self.max_episode_length - 1
        net_contact_forces = self._contact_sensor.data.net_forces_w_history.torch
        died_check_base = torch.any(torch.max(torch.norm(net_contact_forces[:, :, self._base_contact_sensor_id], dim=-1), dim=1)[0] > 1.0, dim=1)
        died_check_hips = torch.any(torch.max(torch.norm(net_contact_forces[:, :, self._hip_contact_sensor_ids], dim=-1), dim=1)[0] > 1.0, dim=1) 
        died = torch.logical_or(died_check_base, died_check_hips)
        return died, time_out


    def _reset_idx(self, env_ids: torch.Tensor | None):
        if env_ids is None or len(env_ids) == self.num_envs:
            env_ids = torch.arange(self.num_envs, device=self.device)

        if(self._terrain.cfg.terrain_generator is not None and self._terrain.cfg.terrain_generator.curriculum == True):
            # Curriculum based on the distance the robot walked
            distance = torch.norm(self._robot.data.root_state_w.torch[env_ids, :2] - self._terrain.env_origins[env_ids, :2], dim=1)
            # robots that walked far enough progress to harder terrains
            move_up = distance > self._terrain.cfg.terrain_generator.size[0] / 2
            # robots that walked less than half of their required distance go to simpler terrains
            move_down = distance < torch.norm(self._commands[env_ids, :2], dim=1) * self.max_episode_length_s * 0.5
            move_down *= ~move_up
            # update terrain levels
            self._terrain.update_env_origins(env_ids, move_up, move_down)

        self._robot.reset(env_ids)
        super()._reset_idx(env_ids)
        if len(env_ids) == self.num_envs: 
            # Spread out the resets to avoid spikes in training when many environments reset at a similar time
            self.episode_length_buf[:] = torch.randint_like(self.episode_length_buf, high=int(self.max_episode_length))
        
        # Reset actions and action filtering
        self._actions[env_ids] = 0.0
        self._previous_actions[env_ids] = 0.0
        self._previous_previous_actions[env_ids] = 0.0
        
        # Reset commands
        custom_events._get_new_random_commands(self, env_ids)

        # Reset swing peak
        self._swing_peak[env_ids] = torch.tensor([0.0, 0.0, 0.0, 0.0], device=self.device)
        self._swing_peak_periodic[env_ids] = torch.tensor([0.0, 0.0, 0.0, 0.0], device=self.device)
        
        # Reset contact periodic
        self._phase_signal[env_ids] = self._phase_offset[env_ids].clone()# + self.step_dt * self._step_freq * torch.rand(env_ids.shape[0], 1, device=self.device)*10.
        self._phase_signal[env_ids] = self._phase_signal[env_ids]  % 1.0

        # Reset observation history
        self._observation_history[env_ids] *= 0.0

        # Reset obs and noise concurrent
        if(self.cfg.use_concurrent_state_est):
            self._observation_history_concurrent_state_est[env_ids] *= 0.0
            if self.cfg.observation_noise_model:
                self._observation_noise_model_concurrent_state_est.reset(env_ids)
        
        # Reset obs and noise rma
        if(self.cfg.use_rma):
            self._observation_history_rma[env_ids] *= 0.0
            if self.cfg.observation_noise_model:
                self._observation_noise_model_rma.reset(env_ids)

        # Reset robot state
        joint_pos = self._robot.data.default_joint_pos.torch[env_ids]
        joint_pos += torch.zeros_like(joint_pos).uniform_(-0.2, 0.2)
        joint_vel = self._robot.data.default_joint_vel.torch[env_ids]
        default_root_state = self._robot.data.default_root_state.torch[env_ids]
        default_root_state[:, :3] += self._terrain.env_origins[env_ids]
        default_root_state[:, 3:7] = math_utils.random_yaw_orientation(env_ids.shape[0], device=self.device)
        self._robot.write_root_pose_to_sim(default_root_state[:, :7], env_ids)
        self._robot.write_root_velocity_to_sim(default_root_state[:, 7:], env_ids)
        self._robot.write_joint_state_to_sim(joint_pos, joint_vel, None, env_ids)
        
        # Logging
        extras = dict()
        for key in self._episode_sums.keys():
            episodic_sum_avg = torch.mean(self._episode_sums[key][env_ids])
            extras["Episode_Reward/" + key] = episodic_sum_avg / self.max_episode_length_s
            self._episode_sums[key][env_ids] = 0.0
        self.extras["log"] = dict()
        self.extras["log"].update(extras)
        extras = dict()
        extras["Episode_Termination/base_contact"] = torch.count_nonzero(self.reset_terminated[env_ids]).item()
        extras["Episode_Termination/time_out"] = torch.count_nonzero(self.reset_time_outs[env_ids]).item()
        
        if(self._terrain.cfg.terrain_generator is not None and self._terrain.cfg.terrain_generator.curriculum == True):
            extras["Episode_Curriculum/terrain_levels"] = torch.mean(self._terrain.terrain_levels.float())
        
        self.extras["log"].update(extras)


    def _set_debug_vis_impl(self, debug_vis: bool):
        custom_rewards._set_debug_vis_impl(self, debug_vis)


    def _debug_vis_callback(self, event):
        custom_rewards._debug_vis_callback(self, event)
