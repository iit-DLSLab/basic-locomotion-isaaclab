// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from dls2_interfaces:msg/BlindState.idl
// generated code does not contain a copyright notice

#ifndef DLS2_INTERFACES__MSG__DETAIL__BLIND_STATE__BUILDER_HPP_
#define DLS2_INTERFACES__MSG__DETAIL__BLIND_STATE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "dls2_interfaces/msg/detail/blind_state__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace dls2_interfaces
{

namespace msg
{

namespace builder
{

class Init_BlindState_current_feet_positions
{
public:
  explicit Init_BlindState_current_feet_positions(::dls2_interfaces::msg::BlindState & msg)
  : msg_(msg)
  {}
  ::dls2_interfaces::msg::BlindState current_feet_positions(::dls2_interfaces::msg::BlindState::_current_feet_positions_type arg)
  {
    msg_.current_feet_positions = std::move(arg);
    return std::move(msg_);
  }

private:
  ::dls2_interfaces::msg::BlindState msg_;
};

class Init_BlindState_feet_contact
{
public:
  explicit Init_BlindState_feet_contact(::dls2_interfaces::msg::BlindState & msg)
  : msg_(msg)
  {}
  Init_BlindState_current_feet_positions feet_contact(::dls2_interfaces::msg::BlindState::_feet_contact_type arg)
  {
    msg_.feet_contact = std::move(arg);
    return Init_BlindState_current_feet_positions(msg_);
  }

private:
  ::dls2_interfaces::msg::BlindState msg_;
};

class Init_BlindState_joints_temperature
{
public:
  explicit Init_BlindState_joints_temperature(::dls2_interfaces::msg::BlindState & msg)
  : msg_(msg)
  {}
  Init_BlindState_feet_contact joints_temperature(::dls2_interfaces::msg::BlindState::_joints_temperature_type arg)
  {
    msg_.joints_temperature = std::move(arg);
    return Init_BlindState_feet_contact(msg_);
  }

private:
  ::dls2_interfaces::msg::BlindState msg_;
};

class Init_BlindState_joints_effort
{
public:
  explicit Init_BlindState_joints_effort(::dls2_interfaces::msg::BlindState & msg)
  : msg_(msg)
  {}
  Init_BlindState_joints_temperature joints_effort(::dls2_interfaces::msg::BlindState::_joints_effort_type arg)
  {
    msg_.joints_effort = std::move(arg);
    return Init_BlindState_joints_temperature(msg_);
  }

private:
  ::dls2_interfaces::msg::BlindState msg_;
};

class Init_BlindState_joints_acceleration
{
public:
  explicit Init_BlindState_joints_acceleration(::dls2_interfaces::msg::BlindState & msg)
  : msg_(msg)
  {}
  Init_BlindState_joints_effort joints_acceleration(::dls2_interfaces::msg::BlindState::_joints_acceleration_type arg)
  {
    msg_.joints_acceleration = std::move(arg);
    return Init_BlindState_joints_effort(msg_);
  }

private:
  ::dls2_interfaces::msg::BlindState msg_;
};

class Init_BlindState_joints_velocity
{
public:
  explicit Init_BlindState_joints_velocity(::dls2_interfaces::msg::BlindState & msg)
  : msg_(msg)
  {}
  Init_BlindState_joints_acceleration joints_velocity(::dls2_interfaces::msg::BlindState::_joints_velocity_type arg)
  {
    msg_.joints_velocity = std::move(arg);
    return Init_BlindState_joints_acceleration(msg_);
  }

private:
  ::dls2_interfaces::msg::BlindState msg_;
};

class Init_BlindState_joints_position
{
public:
  explicit Init_BlindState_joints_position(::dls2_interfaces::msg::BlindState & msg)
  : msg_(msg)
  {}
  Init_BlindState_joints_velocity joints_position(::dls2_interfaces::msg::BlindState::_joints_position_type arg)
  {
    msg_.joints_position = std::move(arg);
    return Init_BlindState_joints_velocity(msg_);
  }

private:
  ::dls2_interfaces::msg::BlindState msg_;
};

class Init_BlindState_joints_name
{
public:
  explicit Init_BlindState_joints_name(::dls2_interfaces::msg::BlindState & msg)
  : msg_(msg)
  {}
  Init_BlindState_joints_position joints_name(::dls2_interfaces::msg::BlindState::_joints_name_type arg)
  {
    msg_.joints_name = std::move(arg);
    return Init_BlindState_joints_position(msg_);
  }

private:
  ::dls2_interfaces::msg::BlindState msg_;
};

class Init_BlindState_robot_name
{
public:
  explicit Init_BlindState_robot_name(::dls2_interfaces::msg::BlindState & msg)
  : msg_(msg)
  {}
  Init_BlindState_joints_name robot_name(::dls2_interfaces::msg::BlindState::_robot_name_type arg)
  {
    msg_.robot_name = std::move(arg);
    return Init_BlindState_joints_name(msg_);
  }

private:
  ::dls2_interfaces::msg::BlindState msg_;
};

class Init_BlindState_timestamp
{
public:
  explicit Init_BlindState_timestamp(::dls2_interfaces::msg::BlindState & msg)
  : msg_(msg)
  {}
  Init_BlindState_robot_name timestamp(::dls2_interfaces::msg::BlindState::_timestamp_type arg)
  {
    msg_.timestamp = std::move(arg);
    return Init_BlindState_robot_name(msg_);
  }

private:
  ::dls2_interfaces::msg::BlindState msg_;
};

class Init_BlindState_sequence_id
{
public:
  explicit Init_BlindState_sequence_id(::dls2_interfaces::msg::BlindState & msg)
  : msg_(msg)
  {}
  Init_BlindState_timestamp sequence_id(::dls2_interfaces::msg::BlindState::_sequence_id_type arg)
  {
    msg_.sequence_id = std::move(arg);
    return Init_BlindState_timestamp(msg_);
  }

private:
  ::dls2_interfaces::msg::BlindState msg_;
};

class Init_BlindState_frame_id
{
public:
  Init_BlindState_frame_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_BlindState_sequence_id frame_id(::dls2_interfaces::msg::BlindState::_frame_id_type arg)
  {
    msg_.frame_id = std::move(arg);
    return Init_BlindState_sequence_id(msg_);
  }

private:
  ::dls2_interfaces::msg::BlindState msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::dls2_interfaces::msg::BlindState>()
{
  return dls2_interfaces::msg::builder::Init_BlindState_frame_id();
}

}  // namespace dls2_interfaces

#endif  // DLS2_INTERFACES__MSG__DETAIL__BLIND_STATE__BUILDER_HPP_
