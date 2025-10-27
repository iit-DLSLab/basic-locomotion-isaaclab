// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from dls2_interfaces:msg/Imu.idl
// generated code does not contain a copyright notice

#ifndef DLS2_INTERFACES__MSG__DETAIL__IMU__BUILDER_HPP_
#define DLS2_INTERFACES__MSG__DETAIL__IMU__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "dls2_interfaces/msg/detail/imu__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace dls2_interfaces
{

namespace msg
{

namespace builder
{

class Init_Imu_linear_acceleration_covariance
{
public:
  explicit Init_Imu_linear_acceleration_covariance(::dls2_interfaces::msg::Imu & msg)
  : msg_(msg)
  {}
  ::dls2_interfaces::msg::Imu linear_acceleration_covariance(::dls2_interfaces::msg::Imu::_linear_acceleration_covariance_type arg)
  {
    msg_.linear_acceleration_covariance = std::move(arg);
    return std::move(msg_);
  }

private:
  ::dls2_interfaces::msg::Imu msg_;
};

class Init_Imu_linear_acceleration
{
public:
  explicit Init_Imu_linear_acceleration(::dls2_interfaces::msg::Imu & msg)
  : msg_(msg)
  {}
  Init_Imu_linear_acceleration_covariance linear_acceleration(::dls2_interfaces::msg::Imu::_linear_acceleration_type arg)
  {
    msg_.linear_acceleration = std::move(arg);
    return Init_Imu_linear_acceleration_covariance(msg_);
  }

private:
  ::dls2_interfaces::msg::Imu msg_;
};

class Init_Imu_angular_velocity_covariance
{
public:
  explicit Init_Imu_angular_velocity_covariance(::dls2_interfaces::msg::Imu & msg)
  : msg_(msg)
  {}
  Init_Imu_linear_acceleration angular_velocity_covariance(::dls2_interfaces::msg::Imu::_angular_velocity_covariance_type arg)
  {
    msg_.angular_velocity_covariance = std::move(arg);
    return Init_Imu_linear_acceleration(msg_);
  }

private:
  ::dls2_interfaces::msg::Imu msg_;
};

class Init_Imu_angular_velocity
{
public:
  explicit Init_Imu_angular_velocity(::dls2_interfaces::msg::Imu & msg)
  : msg_(msg)
  {}
  Init_Imu_angular_velocity_covariance angular_velocity(::dls2_interfaces::msg::Imu::_angular_velocity_type arg)
  {
    msg_.angular_velocity = std::move(arg);
    return Init_Imu_angular_velocity_covariance(msg_);
  }

private:
  ::dls2_interfaces::msg::Imu msg_;
};

class Init_Imu_orientation_covariance
{
public:
  explicit Init_Imu_orientation_covariance(::dls2_interfaces::msg::Imu & msg)
  : msg_(msg)
  {}
  Init_Imu_angular_velocity orientation_covariance(::dls2_interfaces::msg::Imu::_orientation_covariance_type arg)
  {
    msg_.orientation_covariance = std::move(arg);
    return Init_Imu_angular_velocity(msg_);
  }

private:
  ::dls2_interfaces::msg::Imu msg_;
};

class Init_Imu_orientation_rpy
{
public:
  explicit Init_Imu_orientation_rpy(::dls2_interfaces::msg::Imu & msg)
  : msg_(msg)
  {}
  Init_Imu_orientation_covariance orientation_rpy(::dls2_interfaces::msg::Imu::_orientation_rpy_type arg)
  {
    msg_.orientation_rpy = std::move(arg);
    return Init_Imu_orientation_covariance(msg_);
  }

private:
  ::dls2_interfaces::msg::Imu msg_;
};

class Init_Imu_orientation
{
public:
  explicit Init_Imu_orientation(::dls2_interfaces::msg::Imu & msg)
  : msg_(msg)
  {}
  Init_Imu_orientation_rpy orientation(::dls2_interfaces::msg::Imu::_orientation_type arg)
  {
    msg_.orientation = std::move(arg);
    return Init_Imu_orientation_rpy(msg_);
  }

private:
  ::dls2_interfaces::msg::Imu msg_;
};

class Init_Imu_timestamp
{
public:
  explicit Init_Imu_timestamp(::dls2_interfaces::msg::Imu & msg)
  : msg_(msg)
  {}
  Init_Imu_orientation timestamp(::dls2_interfaces::msg::Imu::_timestamp_type arg)
  {
    msg_.timestamp = std::move(arg);
    return Init_Imu_orientation(msg_);
  }

private:
  ::dls2_interfaces::msg::Imu msg_;
};

class Init_Imu_sequence_id
{
public:
  explicit Init_Imu_sequence_id(::dls2_interfaces::msg::Imu & msg)
  : msg_(msg)
  {}
  Init_Imu_timestamp sequence_id(::dls2_interfaces::msg::Imu::_sequence_id_type arg)
  {
    msg_.sequence_id = std::move(arg);
    return Init_Imu_timestamp(msg_);
  }

private:
  ::dls2_interfaces::msg::Imu msg_;
};

class Init_Imu_frame_id
{
public:
  Init_Imu_frame_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Imu_sequence_id frame_id(::dls2_interfaces::msg::Imu::_frame_id_type arg)
  {
    msg_.frame_id = std::move(arg);
    return Init_Imu_sequence_id(msg_);
  }

private:
  ::dls2_interfaces::msg::Imu msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::dls2_interfaces::msg::Imu>()
{
  return dls2_interfaces::msg::builder::Init_Imu_frame_id();
}

}  // namespace dls2_interfaces

#endif  // DLS2_INTERFACES__MSG__DETAIL__IMU__BUILDER_HPP_
