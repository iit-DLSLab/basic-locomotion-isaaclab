// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from dls2_interfaces:msg/TrajectoryGenerator.idl
// generated code does not contain a copyright notice

#ifndef DLS2_INTERFACES__MSG__DETAIL__TRAJECTORY_GENERATOR__BUILDER_HPP_
#define DLS2_INTERFACES__MSG__DETAIL__TRAJECTORY_GENERATOR__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "dls2_interfaces/msg/detail/trajectory_generator__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace dls2_interfaces
{

namespace msg
{

namespace builder
{

class Init_TrajectoryGenerator_normal_force_min
{
public:
  explicit Init_TrajectoryGenerator_normal_force_min(::dls2_interfaces::msg::TrajectoryGenerator & msg)
  : msg_(msg)
  {}
  ::dls2_interfaces::msg::TrajectoryGenerator normal_force_min(::dls2_interfaces::msg::TrajectoryGenerator::_normal_force_min_type arg)
  {
    msg_.normal_force_min = std::move(arg);
    return std::move(msg_);
  }

private:
  ::dls2_interfaces::msg::TrajectoryGenerator msg_;
};

class Init_TrajectoryGenerator_normal_force_max
{
public:
  explicit Init_TrajectoryGenerator_normal_force_max(::dls2_interfaces::msg::TrajectoryGenerator & msg)
  : msg_(msg)
  {}
  Init_TrajectoryGenerator_normal_force_min normal_force_max(::dls2_interfaces::msg::TrajectoryGenerator::_normal_force_max_type arg)
  {
    msg_.normal_force_max = std::move(arg);
    return Init_TrajectoryGenerator_normal_force_min(msg_);
  }

private:
  ::dls2_interfaces::msg::TrajectoryGenerator msg_;
};

class Init_TrajectoryGenerator_swing_period
{
public:
  explicit Init_TrajectoryGenerator_swing_period(::dls2_interfaces::msg::TrajectoryGenerator & msg)
  : msg_(msg)
  {}
  Init_TrajectoryGenerator_normal_force_max swing_period(::dls2_interfaces::msg::TrajectoryGenerator::_swing_period_type arg)
  {
    msg_.swing_period = std::move(arg);
    return Init_TrajectoryGenerator_normal_force_max(msg_);
  }

private:
  ::dls2_interfaces::msg::TrajectoryGenerator msg_;
};

class Init_TrajectoryGenerator_touch_down
{
public:
  explicit Init_TrajectoryGenerator_touch_down(::dls2_interfaces::msg::TrajectoryGenerator & msg)
  : msg_(msg)
  {}
  Init_TrajectoryGenerator_swing_period touch_down(::dls2_interfaces::msg::TrajectoryGenerator::_touch_down_type arg)
  {
    msg_.touch_down = std::move(arg);
    return Init_TrajectoryGenerator_swing_period(msg_);
  }

private:
  ::dls2_interfaces::msg::TrajectoryGenerator msg_;
};

class Init_TrajectoryGenerator_nominal_touch_down
{
public:
  explicit Init_TrajectoryGenerator_nominal_touch_down(::dls2_interfaces::msg::TrajectoryGenerator & msg)
  : msg_(msg)
  {}
  Init_TrajectoryGenerator_touch_down nominal_touch_down(::dls2_interfaces::msg::TrajectoryGenerator::_nominal_touch_down_type arg)
  {
    msg_.nominal_touch_down = std::move(arg);
    return Init_TrajectoryGenerator_touch_down(msg_);
  }

private:
  ::dls2_interfaces::msg::TrajectoryGenerator msg_;
};

class Init_TrajectoryGenerator_stance_legs
{
public:
  explicit Init_TrajectoryGenerator_stance_legs(::dls2_interfaces::msg::TrajectoryGenerator & msg)
  : msg_(msg)
  {}
  Init_TrajectoryGenerator_nominal_touch_down stance_legs(::dls2_interfaces::msg::TrajectoryGenerator::_stance_legs_type arg)
  {
    msg_.stance_legs = std::move(arg);
    return Init_TrajectoryGenerator_nominal_touch_down(msg_);
  }

private:
  ::dls2_interfaces::msg::TrajectoryGenerator msg_;
};

class Init_TrajectoryGenerator_wrench
{
public:
  explicit Init_TrajectoryGenerator_wrench(::dls2_interfaces::msg::TrajectoryGenerator & msg)
  : msg_(msg)
  {}
  Init_TrajectoryGenerator_stance_legs wrench(::dls2_interfaces::msg::TrajectoryGenerator::_wrench_type arg)
  {
    msg_.wrench = std::move(arg);
    return Init_TrajectoryGenerator_stance_legs(msg_);
  }

private:
  ::dls2_interfaces::msg::TrajectoryGenerator msg_;
};

class Init_TrajectoryGenerator_kd
{
public:
  explicit Init_TrajectoryGenerator_kd(::dls2_interfaces::msg::TrajectoryGenerator & msg)
  : msg_(msg)
  {}
  Init_TrajectoryGenerator_wrench kd(::dls2_interfaces::msg::TrajectoryGenerator::_kd_type arg)
  {
    msg_.kd = std::move(arg);
    return Init_TrajectoryGenerator_wrench(msg_);
  }

private:
  ::dls2_interfaces::msg::TrajectoryGenerator msg_;
};

class Init_TrajectoryGenerator_kp
{
public:
  explicit Init_TrajectoryGenerator_kp(::dls2_interfaces::msg::TrajectoryGenerator & msg)
  : msg_(msg)
  {}
  Init_TrajectoryGenerator_kd kp(::dls2_interfaces::msg::TrajectoryGenerator::_kp_type arg)
  {
    msg_.kp = std::move(arg);
    return Init_TrajectoryGenerator_kd(msg_);
  }

private:
  ::dls2_interfaces::msg::TrajectoryGenerator msg_;
};

class Init_TrajectoryGenerator_joints_effort
{
public:
  explicit Init_TrajectoryGenerator_joints_effort(::dls2_interfaces::msg::TrajectoryGenerator & msg)
  : msg_(msg)
  {}
  Init_TrajectoryGenerator_kp joints_effort(::dls2_interfaces::msg::TrajectoryGenerator::_joints_effort_type arg)
  {
    msg_.joints_effort = std::move(arg);
    return Init_TrajectoryGenerator_kp(msg_);
  }

private:
  ::dls2_interfaces::msg::TrajectoryGenerator msg_;
};

class Init_TrajectoryGenerator_joints_acceleration
{
public:
  explicit Init_TrajectoryGenerator_joints_acceleration(::dls2_interfaces::msg::TrajectoryGenerator & msg)
  : msg_(msg)
  {}
  Init_TrajectoryGenerator_joints_effort joints_acceleration(::dls2_interfaces::msg::TrajectoryGenerator::_joints_acceleration_type arg)
  {
    msg_.joints_acceleration = std::move(arg);
    return Init_TrajectoryGenerator_joints_effort(msg_);
  }

private:
  ::dls2_interfaces::msg::TrajectoryGenerator msg_;
};

class Init_TrajectoryGenerator_joints_velocity
{
public:
  explicit Init_TrajectoryGenerator_joints_velocity(::dls2_interfaces::msg::TrajectoryGenerator & msg)
  : msg_(msg)
  {}
  Init_TrajectoryGenerator_joints_acceleration joints_velocity(::dls2_interfaces::msg::TrajectoryGenerator::_joints_velocity_type arg)
  {
    msg_.joints_velocity = std::move(arg);
    return Init_TrajectoryGenerator_joints_acceleration(msg_);
  }

private:
  ::dls2_interfaces::msg::TrajectoryGenerator msg_;
};

class Init_TrajectoryGenerator_joints_position
{
public:
  explicit Init_TrajectoryGenerator_joints_position(::dls2_interfaces::msg::TrajectoryGenerator & msg)
  : msg_(msg)
  {}
  Init_TrajectoryGenerator_joints_velocity joints_position(::dls2_interfaces::msg::TrajectoryGenerator::_joints_position_type arg)
  {
    msg_.joints_position = std::move(arg);
    return Init_TrajectoryGenerator_joints_velocity(msg_);
  }

private:
  ::dls2_interfaces::msg::TrajectoryGenerator msg_;
};

class Init_TrajectoryGenerator_com_acc
{
public:
  explicit Init_TrajectoryGenerator_com_acc(::dls2_interfaces::msg::TrajectoryGenerator & msg)
  : msg_(msg)
  {}
  Init_TrajectoryGenerator_joints_position com_acc(::dls2_interfaces::msg::TrajectoryGenerator::_com_acc_type arg)
  {
    msg_.com_acc = std::move(arg);
    return Init_TrajectoryGenerator_joints_position(msg_);
  }

private:
  ::dls2_interfaces::msg::TrajectoryGenerator msg_;
};

class Init_TrajectoryGenerator_com_vel
{
public:
  explicit Init_TrajectoryGenerator_com_vel(::dls2_interfaces::msg::TrajectoryGenerator & msg)
  : msg_(msg)
  {}
  Init_TrajectoryGenerator_com_acc com_vel(::dls2_interfaces::msg::TrajectoryGenerator::_com_vel_type arg)
  {
    msg_.com_vel = std::move(arg);
    return Init_TrajectoryGenerator_com_acc(msg_);
  }

private:
  ::dls2_interfaces::msg::TrajectoryGenerator msg_;
};

class Init_TrajectoryGenerator_com_pose
{
public:
  explicit Init_TrajectoryGenerator_com_pose(::dls2_interfaces::msg::TrajectoryGenerator & msg)
  : msg_(msg)
  {}
  Init_TrajectoryGenerator_com_vel com_pose(::dls2_interfaces::msg::TrajectoryGenerator::_com_pose_type arg)
  {
    msg_.com_pose = std::move(arg);
    return Init_TrajectoryGenerator_com_vel(msg_);
  }

private:
  ::dls2_interfaces::msg::TrajectoryGenerator msg_;
};

class Init_TrajectoryGenerator_timestamp
{
public:
  explicit Init_TrajectoryGenerator_timestamp(::dls2_interfaces::msg::TrajectoryGenerator & msg)
  : msg_(msg)
  {}
  Init_TrajectoryGenerator_com_pose timestamp(::dls2_interfaces::msg::TrajectoryGenerator::_timestamp_type arg)
  {
    msg_.timestamp = std::move(arg);
    return Init_TrajectoryGenerator_com_pose(msg_);
  }

private:
  ::dls2_interfaces::msg::TrajectoryGenerator msg_;
};

class Init_TrajectoryGenerator_sequence_id
{
public:
  explicit Init_TrajectoryGenerator_sequence_id(::dls2_interfaces::msg::TrajectoryGenerator & msg)
  : msg_(msg)
  {}
  Init_TrajectoryGenerator_timestamp sequence_id(::dls2_interfaces::msg::TrajectoryGenerator::_sequence_id_type arg)
  {
    msg_.sequence_id = std::move(arg);
    return Init_TrajectoryGenerator_timestamp(msg_);
  }

private:
  ::dls2_interfaces::msg::TrajectoryGenerator msg_;
};

class Init_TrajectoryGenerator_frame_id
{
public:
  Init_TrajectoryGenerator_frame_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_TrajectoryGenerator_sequence_id frame_id(::dls2_interfaces::msg::TrajectoryGenerator::_frame_id_type arg)
  {
    msg_.frame_id = std::move(arg);
    return Init_TrajectoryGenerator_sequence_id(msg_);
  }

private:
  ::dls2_interfaces::msg::TrajectoryGenerator msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::dls2_interfaces::msg::TrajectoryGenerator>()
{
  return dls2_interfaces::msg::builder::Init_TrajectoryGenerator_frame_id();
}

}  // namespace dls2_interfaces

#endif  // DLS2_INTERFACES__MSG__DETAIL__TRAJECTORY_GENERATOR__BUILDER_HPP_
