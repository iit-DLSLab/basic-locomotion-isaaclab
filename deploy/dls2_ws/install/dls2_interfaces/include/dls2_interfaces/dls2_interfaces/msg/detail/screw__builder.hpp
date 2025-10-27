// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from dls2_interfaces:msg/Screw.idl
// generated code does not contain a copyright notice

#ifndef DLS2_INTERFACES__MSG__DETAIL__SCREW__BUILDER_HPP_
#define DLS2_INTERFACES__MSG__DETAIL__SCREW__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "dls2_interfaces/msg/detail/screw__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace dls2_interfaces
{

namespace msg
{

namespace builder
{

class Init_Screw_angular
{
public:
  explicit Init_Screw_angular(::dls2_interfaces::msg::Screw & msg)
  : msg_(msg)
  {}
  ::dls2_interfaces::msg::Screw angular(::dls2_interfaces::msg::Screw::_angular_type arg)
  {
    msg_.angular = std::move(arg);
    return std::move(msg_);
  }

private:
  ::dls2_interfaces::msg::Screw msg_;
};

class Init_Screw_linear
{
public:
  Init_Screw_linear()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Screw_angular linear(::dls2_interfaces::msg::Screw::_linear_type arg)
  {
    msg_.linear = std::move(arg);
    return Init_Screw_angular(msg_);
  }

private:
  ::dls2_interfaces::msg::Screw msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::dls2_interfaces::msg::Screw>()
{
  return dls2_interfaces::msg::builder::Init_Screw_linear();
}

}  // namespace dls2_interfaces

#endif  // DLS2_INTERFACES__MSG__DETAIL__SCREW__BUILDER_HPP_
