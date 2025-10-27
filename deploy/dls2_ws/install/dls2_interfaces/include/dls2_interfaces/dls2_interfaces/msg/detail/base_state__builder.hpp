// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from dls2_interfaces:msg/BaseState.idl
// generated code does not contain a copyright notice

#ifndef DLS2_INTERFACES__MSG__DETAIL__BASE_STATE__BUILDER_HPP_
#define DLS2_INTERFACES__MSG__DETAIL__BASE_STATE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "dls2_interfaces/msg/detail/base_state__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace dls2_interfaces
{

namespace msg
{

namespace builder
{

class Init_BaseState_stance_status
{
public:
  explicit Init_BaseState_stance_status(::dls2_interfaces::msg::BaseState & msg)
  : msg_(msg)
  {}
  ::dls2_interfaces::msg::BaseState stance_status(::dls2_interfaces::msg::BaseState::_stance_status_type arg)
  {
    msg_.stance_status = std::move(arg);
    return std::move(msg_);
  }

private:
  ::dls2_interfaces::msg::BaseState msg_;
};

class Init_BaseState_acceleration
{
public:
  explicit Init_BaseState_acceleration(::dls2_interfaces::msg::BaseState & msg)
  : msg_(msg)
  {}
  Init_BaseState_stance_status acceleration(::dls2_interfaces::msg::BaseState::_acceleration_type arg)
  {
    msg_.acceleration = std::move(arg);
    return Init_BaseState_stance_status(msg_);
  }

private:
  ::dls2_interfaces::msg::BaseState msg_;
};

class Init_BaseState_velocity
{
public:
  explicit Init_BaseState_velocity(::dls2_interfaces::msg::BaseState & msg)
  : msg_(msg)
  {}
  Init_BaseState_acceleration velocity(::dls2_interfaces::msg::BaseState::_velocity_type arg)
  {
    msg_.velocity = std::move(arg);
    return Init_BaseState_acceleration(msg_);
  }

private:
  ::dls2_interfaces::msg::BaseState msg_;
};

class Init_BaseState_pose
{
public:
  explicit Init_BaseState_pose(::dls2_interfaces::msg::BaseState & msg)
  : msg_(msg)
  {}
  Init_BaseState_velocity pose(::dls2_interfaces::msg::BaseState::_pose_type arg)
  {
    msg_.pose = std::move(arg);
    return Init_BaseState_velocity(msg_);
  }

private:
  ::dls2_interfaces::msg::BaseState msg_;
};

class Init_BaseState_robot_name
{
public:
  explicit Init_BaseState_robot_name(::dls2_interfaces::msg::BaseState & msg)
  : msg_(msg)
  {}
  Init_BaseState_pose robot_name(::dls2_interfaces::msg::BaseState::_robot_name_type arg)
  {
    msg_.robot_name = std::move(arg);
    return Init_BaseState_pose(msg_);
  }

private:
  ::dls2_interfaces::msg::BaseState msg_;
};

class Init_BaseState_timestamp
{
public:
  explicit Init_BaseState_timestamp(::dls2_interfaces::msg::BaseState & msg)
  : msg_(msg)
  {}
  Init_BaseState_robot_name timestamp(::dls2_interfaces::msg::BaseState::_timestamp_type arg)
  {
    msg_.timestamp = std::move(arg);
    return Init_BaseState_robot_name(msg_);
  }

private:
  ::dls2_interfaces::msg::BaseState msg_;
};

class Init_BaseState_sequence_id
{
public:
  explicit Init_BaseState_sequence_id(::dls2_interfaces::msg::BaseState & msg)
  : msg_(msg)
  {}
  Init_BaseState_timestamp sequence_id(::dls2_interfaces::msg::BaseState::_sequence_id_type arg)
  {
    msg_.sequence_id = std::move(arg);
    return Init_BaseState_timestamp(msg_);
  }

private:
  ::dls2_interfaces::msg::BaseState msg_;
};

class Init_BaseState_frame_id
{
public:
  Init_BaseState_frame_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_BaseState_sequence_id frame_id(::dls2_interfaces::msg::BaseState::_frame_id_type arg)
  {
    msg_.frame_id = std::move(arg);
    return Init_BaseState_sequence_id(msg_);
  }

private:
  ::dls2_interfaces::msg::BaseState msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::dls2_interfaces::msg::BaseState>()
{
  return dls2_interfaces::msg::builder::Init_BaseState_frame_id();
}

}  // namespace dls2_interfaces

#endif  // DLS2_INTERFACES__MSG__DETAIL__BASE_STATE__BUILDER_HPP_
