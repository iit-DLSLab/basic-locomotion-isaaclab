// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from dls2_interfaces:msg/Pose.idl
// generated code does not contain a copyright notice

#ifndef DLS2_INTERFACES__MSG__DETAIL__POSE__STRUCT_HPP_
#define DLS2_INTERFACES__MSG__DETAIL__POSE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__dls2_interfaces__msg__Pose __attribute__((deprecated))
#else
# define DEPRECATED__dls2_interfaces__msg__Pose __declspec(deprecated)
#endif

namespace dls2_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Pose_
{
  using Type = Pose_<ContainerAllocator>;

  explicit Pose_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      std::fill<typename std::array<double, 3>::iterator, double>(this->position.begin(), this->position.end(), 0.0);
      std::fill<typename std::array<double, 4>::iterator, double>(this->orientation.begin(), this->orientation.end(), 0.0);
    }
  }

  explicit Pose_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : position(_alloc),
    orientation(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      std::fill<typename std::array<double, 3>::iterator, double>(this->position.begin(), this->position.end(), 0.0);
      std::fill<typename std::array<double, 4>::iterator, double>(this->orientation.begin(), this->orientation.end(), 0.0);
    }
  }

  // field types and members
  using _position_type =
    std::array<double, 3>;
  _position_type position;
  using _orientation_type =
    std::array<double, 4>;
  _orientation_type orientation;

  // setters for named parameter idiom
  Type & set__position(
    const std::array<double, 3> & _arg)
  {
    this->position = _arg;
    return *this;
  }
  Type & set__orientation(
    const std::array<double, 4> & _arg)
  {
    this->orientation = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    dls2_interfaces::msg::Pose_<ContainerAllocator> *;
  using ConstRawPtr =
    const dls2_interfaces::msg::Pose_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<dls2_interfaces::msg::Pose_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<dls2_interfaces::msg::Pose_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      dls2_interfaces::msg::Pose_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<dls2_interfaces::msg::Pose_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      dls2_interfaces::msg::Pose_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<dls2_interfaces::msg::Pose_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<dls2_interfaces::msg::Pose_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<dls2_interfaces::msg::Pose_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__dls2_interfaces__msg__Pose
    std::shared_ptr<dls2_interfaces::msg::Pose_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__dls2_interfaces__msg__Pose
    std::shared_ptr<dls2_interfaces::msg::Pose_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Pose_ & other) const
  {
    if (this->position != other.position) {
      return false;
    }
    if (this->orientation != other.orientation) {
      return false;
    }
    return true;
  }
  bool operator!=(const Pose_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Pose_

// alias to use template instance with default allocator
using Pose =
  dls2_interfaces::msg::Pose_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace dls2_interfaces

#endif  // DLS2_INTERFACES__MSG__DETAIL__POSE__STRUCT_HPP_
