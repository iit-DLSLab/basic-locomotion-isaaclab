import rclpy 
from rclpy.node import Node 
from dls2_interface.msg import BaseState, BlindState, Imu, TrajectoryGenerator, FeetContactState

import time
import numpy as np
np.set_printoptions(precision=3, suppress=True)

# Gym and Simulation related imports
from gym_quadruped.quadruped_env import QuadrupedEnv
from gym_quadruped.utils.quadruped_utils import LegsAttr

# Config imports
import config as cfg

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
# Set the priority of the process
pid = os.getpid()
print("PID: ", pid)
os.system("renice -n -21 -p " + str(pid))
os.system("echo -20 > /proc/" + str(pid) + "/autogroup")
#for real time, launch it with chrt -r 99 python3 run_controller.py


USE_SCHEDULER = True # Use the scheduler to compute the control signal
SCHEDULER_FREQ = 500 # Frequency of the scheduler
RENDER_FREQ = 30

# Shell for the controllers ----------------------------------------------
class Simulator_Node(Node):
    def __init__(self):
        super().__init__('Simulator_Node')

        # Subscribers and Publishers
        self.publisher_base_state = self.create_publisher(BaseState,"base_state", 1)
        self.publisher_blind_state = self.create_publisher(BlindState,"blind_state", 1)
        self.publisher_imu = self.create_publisher(Imu,"imu", 1)
        self.publisher_feet_contact_state = self.create_publisher(FeetContactState,"feet_contact_state", 1)

        self.subscriber_trajectory_generator = self.create_subscription(TrajectoryGenerator,"trajectory_generator", self.get_trajectory_generator_callback, 1)

        self.timer = self.create_timer(1.0/SCHEDULER_FREQ, self.compute_simulator_step_callback)

        # Timing stuff
        self.loop_time = 0.002
        self.last_start_time = None
        self.last_mpc_loop_time = 0.0


        # Mujoco env
        self.env = QuadrupedEnv(
            robot=cfg.robot,
            scene=cfg.scene,
            sim_dt=1.0/SCHEDULER_FREQ,
            base_vel_command_type="human"
        )
        self.env.reset(random=False)
        

        self.last_render_time = time.time()
        self.env.render()  

        # Desired PD 
        self.desired_joints_position = LegsAttr(*[np.zeros((int(self.env.mjModel.nu/4), 1)) for _ in range(4)])
        self.desired_joints_velocity = LegsAttr(*[np.zeros((int(self.env.mjModel.nu/4), 1)) for _ in range(4)])

        # Desired gains
        self.Kp = 0
        self.Kd = 0


    def get_trajectory_generator_callback(self, msg):

        joints_position = np.array(msg.joints_position)

        self.desired_joints_position.FL = joints_position[0:3]
        self.desired_joints_position.FR = joints_position[3:6]
        self.desired_joints_position.RL = joints_position[6:9]
        self.desired_joints_position.RR = joints_position[9:12]

        self.Kp = np.array(msg.kp)[0]
        self.Kd = np.array(msg.kd)[0]
        

    def compute_simulator_step_callback(self):

        qpos, qvel = self.env.mjData.qpos, self.env.mjData.qvel
        base_lin_vel = self.env.base_lin_vel(frame='world')
        base_ang_vel = self.env.base_ang_vel(frame='base')
        base_pos = self.env.base_pos

        # Publish Base State ------------------------------------------------
        base_state_msg = BaseState()
        base_state_msg.pose.position = base_pos
        base_state_msg.pose.orientation = np.roll(self.env.mjData.qpos[3:7],-1)
        base_state_msg.velocity.linear = base_lin_vel
        base_state_msg.velocity.angular = base_ang_vel
        self.publisher_base_state.publish(base_state_msg)


        # Publish Blind State ------------------------------------------------
        blind_state_msg = BlindState()
        blind_state_msg.joints_position = self.env.mjData.qpos[7:].tolist()
        blind_state_msg.joints_velocity = self.env.mjData.qvel[6:].tolist()
        self.publisher_blind_state.publish(blind_state_msg)


        # Publish IMU ------------------------------------------------
        imu_msg = Imu()
        imu_msg.linear_acceleration = self.env.mjData.sensordata[0:3]
        imu_msg.angular_velocity = self.env.mjData.sensordata[3:6]
        imu_msg.orientation = self.env.mjData.sensordata[9:13]
        self.publisher_imu.publish(imu_msg)


        # Publish Feet Contact State ------------------------------------------------
        _, _, feet_GRF = self.env.feet_contact_state(ground_reaction_forces=True)
        feet_contact_state_msg = FeetContactState()
        feet_contact_state_msg.feet_name = ["FL", "FR", "RL", "RR"]
        feet_contact_state_msg.linear_grf_feet = np.concatenate([feet_GRF["FL"], feet_GRF["FR"], feet_GRF["RL"], feet_GRF["RR"]]).tolist()
        feet_contact_state_msg.angular_grf_feet = np.concatenate([feet_GRF["FL"]*0.0, feet_GRF["FR"]*0.0, feet_GRF["RL"]*0.0, feet_GRF["RR"]*0.0]).tolist()
        self.publisher_feet_contact_state.publish(feet_contact_state_msg)


        # Step the environment --------------------------------------------------------------------------------
        joints_pos = LegsAttr(*[np.zeros((1, int(self.env.mjModel.nu/4))) for _ in range(4)])
        joints_pos.FL = qpos[self.env.legs_qpos_idx.FL]
        joints_pos.FR = qpos[self.env.legs_qpos_idx.FR]
        joints_pos.RL = qpos[self.env.legs_qpos_idx.RL]
        joints_pos.RR = qpos[self.env.legs_qpos_idx.RR]


        joints_vel = LegsAttr(*[np.zeros((1, int(self.env.mjModel.nu/4))) for _ in range(4)])
        joints_vel.FL = qvel[self.env.legs_qvel_idx.FL]
        joints_vel.FR = qvel[self.env.legs_qvel_idx.FR]
        joints_vel.RL = qvel[self.env.legs_qvel_idx.RL]
        joints_vel.RR = qvel[self.env.legs_qvel_idx.RR]


        action = np.zeros(self.env.mjModel.nu)
        action[self.env.legs_tau_idx.FL] = self.Kp*(self.desired_joints_position.FL.reshape(-1) - joints_pos.FL) - self.Kd*(joints_vel.FL)
        action[self.env.legs_tau_idx.FR] = self.Kp*(self.desired_joints_position.FR.reshape(-1) - joints_pos.FR) - self.Kd*(joints_vel.FR)
        action[self.env.legs_tau_idx.RL] = self.Kp*(self.desired_joints_position.RL.reshape(-1) - joints_pos.RL) - self.Kd*(joints_vel.RL)
        action[self.env.legs_tau_idx.RR] = self.Kp*(self.desired_joints_position.RR.reshape(-1) - joints_pos.RR) - self.Kd*(joints_vel.RR)
        self.env.step(action=action)


        # Render only at a certain frequency -----------------------------------------------------------------
        if time.time() - self.last_render_time > 1.0 / RENDER_FREQ:
            self.env.render()
            self.last_render_time = time.time()


def main():
    print('Hello from the gym_quadruped simulator.')
    rclpy.init()

    simulator_node = Simulator_Node()

    rclpy.spin(simulator_node)
    simulator_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
