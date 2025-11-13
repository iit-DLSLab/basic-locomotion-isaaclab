// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from dls2_interfaces:msg/Imu.idl
// generated code does not contain a copyright notice

#ifndef DLS2_INTERFACES__MSG__DETAIL__IMU__STRUCT_HPP_
#define DLS2_INTERFACES__MSG__DETAIL__IMU__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__dls2_interfaces__msg__Imu __attribute__((deprecated))
#else
# define DEPRECATED__dls2_interfaces__msg__Imu __declspec(deprecated)
#endif

namespace dls2_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Imu_
{
  using Type = Imu_<ContainerAllocator>;

  explicit Imu_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->frame_id = "";
      this->sequence_id = 0ul;
      this->timestamp = 0.0;
      std::fill<typename std::array<double, 4>::iterator, double>(this->orientation.begin(), this->orientation.end(), 0.0);
      std::fill<typename std::array<double, 9>::iterator, double>(this->orientation_covariance.begin(), this->orientation_covariance.end(), 0.0);
      std::fill<typename std::array<double, 3>::iterator, double>(this->angular_velocity.begin(), this->angular_velocity.end(), 0.0);
      std::fill<typename std::array<double, 9>::iterator, double>(this->angular_velocity_covariance.begin(), this->angular_velocity_covariance.end(), 0.0);
      std::fill<typename std::array<double, 3>::iterator, double>(this->linear_acceleration.begin(), this->linear_acceleration.end(), 0.0);
      std::fill<typename std::array<double, 9>::iterator, double>(this->linear_acceleration_covariance.begin(), this->linear_acceleration_covariance.end(), 0.0);
    }
  }

  explicit Imu_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : frame_id(_alloc),
    orientation(_alloc),
    orientation_covariance(_alloc),
    angular_velocity(_alloc),
    angular_velocity_covariance(_alloc),
    linear_acceleration(_alloc),
    linear_acceleration_covariance(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->frame_id = "";
      this->sequence_id = 0ul;
      this->timestamp = 0.0;
      std::fill<typename std::array<double, 4>::iterator, double>(this->orientation.begin(), this->orientation.end(), 0.0);
      std::fill<typename std::array<double, 9>::iterator, double>(this->orientation_covariance.begin(), this->orientation_covariance.end(), 0.0);
      std::fill<typename std::array<double, 3>::iterator, double>(this->angular_velocity.begin(), this->angular_velocity.end(), 0.0);
      std::fill<typename std::array<double, 9>::iterator, double>(this->angular_velocity_covariance.begin(), this->angular_velocity_covariance.end(), 0.0);
      std::fill<typename std::array<double, 3>::iterator, double>(this->linear_acceleration.begin(), this->linear_acceleration.end(), 0.0);
      std::fill<typename std::array<double, 9>::iterator, double>(this->linear_acceleration_covariance.begin(), this->linear_acceleration_covariance.end(), 0.0);
    }
  }

  // field types and members
  using _frame_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _frame_id_type frame_id;
  using _sequence_id_type =
    uint32_t;
  _sequence_id_type sequence_id;
  using _timestamp_type =
    double;
  _timestamp_type timestamp;
  using _orientation_type =
    std::array<double, 4>;
  _orientation_type orientation;
  using _orientation_covariance_type =
    std::array<double, 9>;
  _orientation_covariance_type orientation_covariance;
  using _angular_velocity_type =
    std::array<double, 3>;
  _angular_velocity_type angular_velocity;
  using _angular_velocity_covariance_type =
    std::array<double, 9>;
  _angular_velocity_covariance_type angular_velocity_covariance;
  using _linear_acceleration_type =
    std::array<double, 3>;
  _linear_acceleration_type linear_acceleration;
  using _linear_acceleration_covariance_type =
    std::array<double, 9>;
  _linear_acceleration_covariance_type linear_acceleration_covariance;

  // setters for named parameter idiom
  Type & set__frame_id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->frame_id = _arg;
    return *this;
  }
  Type & set__sequence_id(
    const uint32_t & _arg)
  {
    this->sequence_id = _arg;
    return *this;
  }
  Type & set__timestamp(
    const double & _arg)
  {
    this->timestamp = _arg;
    return *this;
  }
  Type & set__orientation(
    const std::array<double, 4> & _arg)
  {
    this->orientation = _arg;
    return *this;
  }
  Type & set__orientation_covariance(
    const std::array<double, 9> & _arg)
  {
    this->orientation_covariance = _arg;
    return *this;
  }
  Type & set__angular_velocity(
    const std::array<double, 3> & _arg)
  {
    this->angular_velocity = _arg;
    return *this;
  }
  Type & set__angular_velocity_covariance(
    const std::array<double, 9> & _arg)
  {
    this->angular_velocity_covariance = _arg;
    return *this;
  }
  Type & set__linear_acceleration(
    const std::array<double, 3> & _arg)
  {
    this->linear_acceleration = _arg;
    return *this;
  }
  Type & set__linear_acceleration_covariance(
    const std::array<double, 9> & _arg)
  {
    this->linear_acceleration_covariance = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    dls2_interfaces::msg::Imu_<ContainerAllocator> *;
  using ConstRawPtr =
    const dls2_interfaces::msg::Imu_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<dls2_interfaces::msg::Imu_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<dls2_interfaces::msg::Imu_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      dls2_interfaces::msg::Imu_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<dls2_interfaces::msg::Imu_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      dls2_interfaces::msg::Imu_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<dls2_interfaces::msg::Imu_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<dls2_interfaces::msg::Imu_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<dls2_interfaces::msg::Imu_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__dls2_interfaces__msg__Imu
    std::shared_ptr<dls2_interfaces::msg::Imu_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__dls2_interfaces__msg__Imu
    std::shared_ptr<dls2_interfaces::msg::Imu_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Imu_ & other) const
  {
    if (this->frame_id != other.frame_id) {
      return false;
    }
    if (this->sequence_id != other.sequence_id) {
      return false;
    }
    if (this->timestamp != other.timestamp) {
      return false;
    }
    if (this->orientation != other.orientation) {
      return false;
    }
    if (this->orientation_covariance != other.orientation_covariance) {
      return false;
    }
    if (this->angular_velocity != other.angular_velocity) {
      return false;
    }
    if (this->angular_velocity_covariance != other.angular_velocity_covariance) {
      return false;
    }
    if (this->linear_acceleration != other.linear_acceleration) {
      return false;
    }
    if (this->linear_acceleration_covariance != other.linear_acceleration_covariance) {
      return false;
    }
    return true;
  }
  bool operator!=(const Imu_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Imu_

// alias to use template instance with default allocator
using Imu =
  dls2_interfaces::msg::Imu_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace dls2_interfaces

#endif  // DLS2_INTERFACES__MSG__DETAIL__IMU__STRUCT_HPP_
