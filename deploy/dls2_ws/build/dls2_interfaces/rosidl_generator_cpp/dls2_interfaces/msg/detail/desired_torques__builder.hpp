// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from dls2_interfaces:msg/DesiredTorques.idl
// generated code does not contain a copyright notice

#ifndef DLS2_INTERFACES__MSG__DETAIL__DESIRED_TORQUES__BUILDER_HPP_
#define DLS2_INTERFACES__MSG__DETAIL__DESIRED_TORQUES__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "dls2_interfaces/msg/detail/desired_torques__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace dls2_interfaces
{

namespace msg
{

namespace builder
{

class Init_DesiredTorques_desired_torques
{
public:
  explicit Init_DesiredTorques_desired_torques(::dls2_interfaces::msg::DesiredTorques & msg)
  : msg_(msg)
  {}
  ::dls2_interfaces::msg::DesiredTorques desired_torques(::dls2_interfaces::msg::DesiredTorques::_desired_torques_type arg)
  {
    msg_.desired_torques = std::move(arg);
    return std::move(msg_);
  }

private:
  ::dls2_interfaces::msg::DesiredTorques msg_;
};

class Init_DesiredTorques_timestamp
{
public:
  explicit Init_DesiredTorques_timestamp(::dls2_interfaces::msg::DesiredTorques & msg)
  : msg_(msg)
  {}
  Init_DesiredTorques_desired_torques timestamp(::dls2_interfaces::msg::DesiredTorques::_timestamp_type arg)
  {
    msg_.timestamp = std::move(arg);
    return Init_DesiredTorques_desired_torques(msg_);
  }

private:
  ::dls2_interfaces::msg::DesiredTorques msg_;
};

class Init_DesiredTorques_sequence_id
{
public:
  explicit Init_DesiredTorques_sequence_id(::dls2_interfaces::msg::DesiredTorques & msg)
  : msg_(msg)
  {}
  Init_DesiredTorques_timestamp sequence_id(::dls2_interfaces::msg::DesiredTorques::_sequence_id_type arg)
  {
    msg_.sequence_id = std::move(arg);
    return Init_DesiredTorques_timestamp(msg_);
  }

private:
  ::dls2_interfaces::msg::DesiredTorques msg_;
};

class Init_DesiredTorques_frame_id
{
public:
  Init_DesiredTorques_frame_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_DesiredTorques_sequence_id frame_id(::dls2_interfaces::msg::DesiredTorques::_frame_id_type arg)
  {
    msg_.frame_id = std::move(arg);
    return Init_DesiredTorques_sequence_id(msg_);
  }

private:
  ::dls2_interfaces::msg::DesiredTorques msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::dls2_interfaces::msg::DesiredTorques>()
{
  return dls2_interfaces::msg::builder::Init_DesiredTorques_frame_id();
}

}  // namespace dls2_interfaces

#endif  // DLS2_INTERFACES__MSG__DETAIL__DESIRED_TORQUES__BUILDER_HPP_
