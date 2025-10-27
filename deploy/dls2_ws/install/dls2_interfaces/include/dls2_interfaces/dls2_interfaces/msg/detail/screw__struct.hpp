// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from dls2_interfaces:msg/Screw.idl
// generated code does not contain a copyright notice

#ifndef DLS2_INTERFACES__MSG__DETAIL__SCREW__STRUCT_HPP_
#define DLS2_INTERFACES__MSG__DETAIL__SCREW__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__dls2_interfaces__msg__Screw __attribute__((deprecated))
#else
# define DEPRECATED__dls2_interfaces__msg__Screw __declspec(deprecated)
#endif

namespace dls2_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Screw_
{
  using Type = Screw_<ContainerAllocator>;

  explicit Screw_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      std::fill<typename std::array<double, 3>::iterator, double>(this->linear.begin(), this->linear.end(), 0.0);
      std::fill<typename std::array<double, 3>::iterator, double>(this->angular.begin(), this->angular.end(), 0.0);
    }
  }

  explicit Screw_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : linear(_alloc),
    angular(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      std::fill<typename std::array<double, 3>::iterator, double>(this->linear.begin(), this->linear.end(), 0.0);
      std::fill<typename std::array<double, 3>::iterator, double>(this->angular.begin(), this->angular.end(), 0.0);
    }
  }

  // field types and members
  using _linear_type =
    std::array<double, 3>;
  _linear_type linear;
  using _angular_type =
    std::array<double, 3>;
  _angular_type angular;

  // setters for named parameter idiom
  Type & set__linear(
    const std::array<double, 3> & _arg)
  {
    this->linear = _arg;
    return *this;
  }
  Type & set__angular(
    const std::array<double, 3> & _arg)
  {
    this->angular = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    dls2_interfaces::msg::Screw_<ContainerAllocator> *;
  using ConstRawPtr =
    const dls2_interfaces::msg::Screw_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<dls2_interfaces::msg::Screw_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<dls2_interfaces::msg::Screw_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      dls2_interfaces::msg::Screw_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<dls2_interfaces::msg::Screw_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      dls2_interfaces::msg::Screw_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<dls2_interfaces::msg::Screw_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<dls2_interfaces::msg::Screw_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<dls2_interfaces::msg::Screw_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__dls2_interfaces__msg__Screw
    std::shared_ptr<dls2_interfaces::msg::Screw_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__dls2_interfaces__msg__Screw
    std::shared_ptr<dls2_interfaces::msg::Screw_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Screw_ & other) const
  {
    if (this->linear != other.linear) {
      return false;
    }
    if (this->angular != other.angular) {
      return false;
    }
    return true;
  }
  bool operator!=(const Screw_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Screw_

// alias to use template instance with default allocator
using Screw =
  dls2_interfaces::msg::Screw_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace dls2_interfaces

#endif  // DLS2_INTERFACES__MSG__DETAIL__SCREW__STRUCT_HPP_
