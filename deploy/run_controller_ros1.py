# Description: This script is used to run the policy on the real robot

# Authors:
# Giulio Turrisi

import rospy
from dls_msgs.msg import rl_signal_in, rl_signal_out

import time
import numpy as np
np.set_printoptions(precision=3, suppress=True)

import threading

import copy

# Gym and Simulation related imports
import mujoco
from gym_quadruped.quadruped_env import QuadrupedEnv
from gym_quadruped.utils.quadruped_utils import LegsAttr

import sys
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path+"/../")

# Locomotion Policy imports
from locomotion_policy_wrapper import LocomotionPolicyWrapper

import config

# Set the priority of the process
pid = os.getpid()
print("PID: ", pid)
os.system("renice -n -21 -p " + str(pid))
os.system("echo -20 > /proc/" + str(pid) + "/autogroup")
#for real time, launch it with chrt -r 99 python3 run_controller.py

USE_MUJOCO_RENDER = False
USE_MUJOCO_SIMULATION = False

USE_SMOOTH_VELOCITY = True

class Basic_Locomotion_DLS_Isaaclab_Node():
    def __init__(self):

        # Mujoco env
        robot_name = config.robot
        scene_name = config.scene
        simulation_dt = 0.002


        # Create the quadruped robot environment -----------------------------------------------------------
        self.env = QuadrupedEnv(
            robot=robot_name,
            scene=scene_name,
            sim_dt=simulation_dt,
            base_vel_command_type="human",  # "forward", "random", "forward+rotate", "human"
        )
        self.env.reset(random=False)
        
        self.last_render_time = time.time()
        if USE_MUJOCO_RENDER:
            self.env.render()

        
        # Subscribers and Publishers
        self.subscription_state = rospy.Subscriber("/rl/rl_signal_in", rl_signal_in, self.get_state_callback, tcp_nodelay=True, queue_size=1)
        self.publisher = rospy.Publisher('/rl/rl_signal_out', rl_signal_out, queue_size=1)
        RL_FREQ = 1./(config.training_env["sim"]["dt"]*config.training_env["decimation"])  # Hz, frequency of the RL controller
        self.timer = rospy.Timer(rospy.Duration(1.0/RL_FREQ), self.compute_rl_control)

        # Safety check to not do anything until a first base and blind state are received
        self.first_message_base_arrived = False
        self.first_message_joints_arrived = False 

        # Timing stuff
        self.loop_time = 0.002
        self.last_start_time = None

        # Base State
        self.position = np.zeros(3)
        self.orientation = np.zeros(4)
        self.linear_velocity = np.zeros(3)
        self.angular_velocity = np.zeros(3)

        # Blind State
        self.joint_positions = np.zeros(12)
        self.joint_velocities = np.zeros(12)

        
        # Initialization of variables used in the main control loop --------------------------------
        self.locomotion_policy = LocomotionPolicyWrapper(env=self.env)


        self.stand_up_and_down_actions = LegsAttr(*[np.zeros((1, int(self.env.mjModel.nu/4))) for _ in range(4)])
        keyframe_id = mujoco.mj_name2id(self.env.mjModel, mujoco.mjtObj.mjOBJ_KEY, "down")
        goDown_qpos = self.env.mjModel.key_qpos[keyframe_id]
        self.stand_up_and_down_actions.FL = goDown_qpos[7:10]
        self.stand_up_and_down_actions.FR = goDown_qpos[10:13]
        self.stand_up_and_down_actions.RL = goDown_qpos[13:16]
        self.stand_up_and_down_actions.RR = goDown_qpos[16:19]
        self.joint_positions = goDown_qpos[7:19]


        # Interactive Command Line ----------------------------
        from console import Console
        self.console = Console(controller_node=self)
        thread_console = threading.Thread(target=self.console.interactive_command_line)
        thread_console.daemon = True
        thread_console.start()

        self.console.isDown = False
        self.console.isRLActivated = True


    def get_state_callback(self, msg):
        
        self.position = np.array(msg.position) #world frame
        # For the quaternion, the order is [w, x, y, z] on mujoco, and [x, y, z, w] on DLS1
        self.orientation = np.roll(np.array(msg.orientation_quat), 1) #world frame
        self.linear_velocity = np.array(msg.linear_velocity) #world frame
        self.angular_velocity = np.array(msg.angular_velocity) #base frame

        self.joint_positions = np.array(msg.joint_positions)
        self.joint_velocities = np.array(msg.joint_velocities)

        if(config.robot == "aliengo"):
            # Fix convention
            self.joint_positions[0] = -self.joint_positions[0]
            self.joint_positions[6] = -self.joint_positions[6]
            self.joint_velocities[0] = -self.joint_velocities[0]
            self.joint_velocities[6] = -self.joint_velocities[6]

        self.first_message_base_arrived = True
        self.first_message_joints_arrived = True


    def compute_rl_control(self, event):
        
        # Update the loop time
        start_time = time.perf_counter()
        if(self.last_start_time is not None):
            self.loop_time = (start_time - self.last_start_time)
        self.last_start_time = start_time
        simulation_dt = self.loop_time

        # Safety check to not do anything until a first base and blind state are received
        if(not USE_MUJOCO_SIMULATION and self.first_message_base_arrived==False and self.first_message_joints_arrived==False):
            return

        old_base_lin_vel = self.env.base_lin_vel(frame='base')

        # Update the mujoco model
        if(not USE_MUJOCO_SIMULATION):
            self.env.mjData.qpos[0:3] = copy.deepcopy(self.position)
            self.env.mjData.qpos[3:7] = copy.deepcopy(self.orientation)
            self.env.mjData.qvel[0:3] = copy.deepcopy(self.linear_velocity)
            self.env.mjData.qvel[3:6] = copy.deepcopy(self.angular_velocity)
            self.env.mjData.qpos[7:] = copy.deepcopy(self.joint_positions)
            self.env.mjData.qvel[6:] = copy.deepcopy(self.joint_velocities)
            self.env.mjModel.opt.timestep = simulation_dt
            mujoco.mj_forward(self.env.mjModel, self.env.mjData)     

        env = self.env
        locomotion_policy = self.locomotion_policy
        
        qpos, qvel = env.mjData.qpos, env.mjData.qvel
        base_lin_vel = env.base_lin_vel(frame='base')
        base_ang_vel = env.base_ang_vel(frame='base')
        base_ori_euler_xyz = env.base_ori_euler_xyz
        heading_orientation_SO3 = env.heading_orientation_SO3
        base_quat_wxyz = qpos[3:7]
        base_pos = env.base_pos

        if(USE_SMOOTH_VELOCITY):
            base_lin_vel = 0.5*base_lin_vel + 0.5*old_base_lin_vel

        joints_pos = LegsAttr(*[np.zeros((1, int(env.mjModel.nu/4))) for _ in range(4)])
        joints_pos.FL = qpos[env.legs_qpos_idx.FL]
        joints_pos.FR = qpos[env.legs_qpos_idx.FR]
        joints_pos.RL = qpos[env.legs_qpos_idx.RL]
        joints_pos.RR = qpos[env.legs_qpos_idx.RR]

        # variable saved for goDown and goUp motion
        self.joint_positions = np.concatenate([joints_pos.FL, joints_pos.FR, joints_pos.RL, joints_pos.RR], axis=0).flatten()
    
        joints_vel = LegsAttr(*[np.zeros((1, int(env.mjModel.nu/4))) for _ in range(4)])
        joints_vel.FL = qvel[env.legs_qvel_idx.FL]
        joints_vel.FR = qvel[env.legs_qvel_idx.FR]
        joints_vel.RL = qvel[env.legs_qvel_idx.RL]
        joints_vel.RR = qvel[env.legs_qvel_idx.RR]
        ref_base_lin_vel, ref_base_ang_vel = env.target_base_vel()


        if(self.console.isDown):
            desired_joint_pos = LegsAttr(*[np.zeros((1, int(env.mjModel.nu/4))) for _ in range(4)])
            desired_joint_pos.FL = self.stand_up_and_down_actions.FL
            desired_joint_pos.FR = self.stand_up_and_down_actions.FR
            desired_joint_pos.RL = self.stand_up_and_down_actions.RL
            desired_joint_pos.RR = self.stand_up_and_down_actions.RR

            # Impedence Loop
            Kp = locomotion_policy.Kp_stand_up_and_down
            Kd = locomotion_policy.Kd_stand_up_and_down
            

        elif(self.console.isRLActivated):

            desired_joint_pos = locomotion_policy.compute_control(
                        base_pos=base_pos, 
                        base_ori_euler_xyz=base_ori_euler_xyz, 
                        base_quat_wxyz=base_quat_wxyz,
                        base_lin_vel=base_lin_vel, 
                        base_ang_vel=base_ang_vel,
                        heading_orientation_SO3=heading_orientation_SO3,
                        joints_pos=joints_pos, 
                        joints_vel=joints_vel,
                        ref_base_lin_vel=ref_base_lin_vel, 
                        ref_base_ang_vel=ref_base_ang_vel)

            # Impedence Loop
            Kp = locomotion_policy.Kp_walking
            Kd = locomotion_policy.Kd_walking


        else:
            return

        if USE_MUJOCO_SIMULATION:
            for j in range(10): #Hardcoded for now, if RL is 50Hz, this runs the simulation at 500Hz
                joints_pos.FL = qpos[env.legs_qpos_idx.FL]
                joints_pos.FR = qpos[env.legs_qpos_idx.FR]
                joints_pos.RL = qpos[env.legs_qpos_idx.RL]
                joints_pos.RR = qpos[env.legs_qpos_idx.RR]
            
                joints_vel.FL = qvel[env.legs_qvel_idx.FL]
                joints_vel.FR = qvel[env.legs_qvel_idx.FR]
                joints_vel.RL = qvel[env.legs_qvel_idx.RL]
                joints_vel.RR = qvel[env.legs_qvel_idx.RR]

                error_joints_pos = LegsAttr(*[np.zeros((1, int(env.mjModel.nu/4))) for _ in range(4)])
                error_joints_pos.FL = desired_joint_pos.FL - joints_pos.FL
                error_joints_pos.FR = desired_joint_pos.FR - joints_pos.FR
                error_joints_pos.RL = desired_joint_pos.RL - joints_pos.RL
                error_joints_pos.RR = desired_joint_pos.RR - joints_pos.RR
                
                tau = LegsAttr(*[np.zeros((1, int(env.mjModel.nu/4))) for _ in range(4)])
                tau.FL = Kp * (error_joints_pos.FL) - Kd * joints_vel.FL
                tau.FR = Kp * (error_joints_pos.FR) - Kd * joints_vel.FR
                tau.RL = Kp * (error_joints_pos.RL) - Kd * joints_vel.RL
                tau.RR = Kp * (error_joints_pos.RR) - Kd * joints_vel.RR

                action = np.zeros(self.env.mjModel.nu)
                action[self.env.legs_tau_idx.FL] = tau.FL.reshape((3,))
                action[self.env.legs_tau_idx.FR] = tau.FR.reshape((3,))
                action[self.env.legs_tau_idx.RL] = tau.RL.reshape((3,))
                action[self.env.legs_tau_idx.RR] = tau.RR.reshape((3,))
                self.env.step(action=action)
 
 
        if(config.robot == "aliengo"):
            # Fix convention
            desired_joint_pos.FL[0] = -desired_joint_pos.FL[0]
            desired_joint_pos.RL[0] = -desired_joint_pos.RL[0] 

        rl_signal_out_msg = rl_signal_out()
        rl_signal_out_msg.kp = np.ones(12)*Kp
        rl_signal_out_msg.kd = np.ones(12)*Kd
        rl_signal_out_msg.desired_joint_positions = np.concatenate([desired_joint_pos.FL, desired_joint_pos.FR, desired_joint_pos.RL, desired_joint_pos.RR], axis=0).flatten()
        self.publisher.publish(rl_signal_out_msg)
        
        
        
        # Render the simulation -----------------------------------------------------------------------------------
        if USE_MUJOCO_RENDER:
            RENDER_FREQ = 30
            # Render only at a certain frequency -----------------------------------------------------------------
            if time.time() - self.last_render_time > 1.0 / RENDER_FREQ or self.env.step_num == 1:
                self.env.render()
                self.last_render_time = time.time()




#---------------------------
if __name__ == '__main__':
    
    print('Hello from basic-locomotion-dls-isaaclab ros node.')
    
    rospy.init_node('basic_locomotion_dls_isaaclab_node', anonymous=True)
    basic_locomotion_dls_isaaclab_node = Basic_Locomotion_DLS_Isaaclab_Node()
    rospy.spin()

    print("basic-locomotion-dls-isaaclab ros node is stopped")
    exit(0)