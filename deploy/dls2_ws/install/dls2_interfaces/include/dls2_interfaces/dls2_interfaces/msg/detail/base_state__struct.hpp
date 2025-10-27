// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from dls2_interfaces:msg/BaseState.idl
// generated code does not contain a copyright notice

#ifndef DLS2_INTERFACES__MSG__DETAIL__BASE_STATE__STRUCT_HPP_
#define DLS2_INTERFACES__MSG__DETAIL__BASE_STATE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'pose'
#include "dls2_interfaces/msg/detail/pose__struct.hpp"
// Member 'velocity'
// Member 'acceleration'
#include "dls2_interfaces/msg/detail/screw__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__dls2_interfaces__msg__BaseState __attribute__((deprecated))
#else
# define DEPRECATED__dls2_interfaces__msg__BaseState __declspec(deprecated)
#endif

namespace dls2_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct BaseState_
{
  using Type = BaseState_<ContainerAllocator>;

  explicit BaseState_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : pose(_init),
    velocity(_init),
    acceleration(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->frame_id = "";
      this->sequence_id = 0ul;
      this->timestamp = 0.0;
      this->robot_name = "";
    }
  }

  explicit BaseState_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : frame_id(_alloc),
    robot_name(_alloc),
    pose(_alloc, _init),
    velocity(_alloc, _init),
    acceleration(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->frame_id = "";
      this->sequence_id = 0ul;
      this->timestamp = 0.0;
      this->robot_name = "";
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
  using _robot_name_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _robot_name_type robot_name;
  using _pose_type =
    dls2_interfaces::msg::Pose_<ContainerAllocator>;
  _pose_type pose;
  using _velocity_type =
    dls2_interfaces::msg::Screw_<ContainerAllocator>;
  _velocity_type velocity;
  using _acceleration_type =
    dls2_interfaces::msg::Screw_<ContainerAllocator>;
  _acceleration_type acceleration;
  using _stance_status_type =
    std::vector<bool, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<bool>>;
  _stance_status_type stance_status;

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
  Type & set__robot_name(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->robot_name = _arg;
    return *this;
  }
  Type & set__pose(
    const dls2_interfaces::msg::Pose_<ContainerAllocator> & _arg)
  {
    this->pose = _arg;
    return *this;
  }
  Type & set__velocity(
    const dls2_interfaces::msg::Screw_<ContainerAllocator> & _arg)
  {
    this->velocity = _arg;
    return *this;
  }
  Type & set__acceleration(
    const dls2_interfaces::msg::Screw_<ContainerAllocator> & _arg)
  {
    this->acceleration = _arg;
    return *this;
  }
  Type & set__stance_status(
    const std::vector<bool, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<bool>> & _arg)
  {
    this->stance_status = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    dls2_interfaces::msg::BaseState_<ContainerAllocator> *;
  using ConstRawPtr =
    const dls2_interfaces::msg::BaseState_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<dls2_interfaces::msg::BaseState_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<dls2_interfaces::msg::BaseState_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      dls2_interfaces::msg::BaseState_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<dls2_interfaces::msg::BaseState_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      dls2_interfaces::msg::BaseState_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<dls2_interfaces::msg::BaseState_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<dls2_interfaces::msg::BaseState_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<dls2_interfaces::msg::BaseState_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__dls2_interfaces__msg__BaseState
    std::shared_ptr<dls2_interfaces::msg::BaseState_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__dls2_interfaces__msg__BaseState
    std::shared_ptr<dls2_interfaces::msg::BaseState_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const BaseState_ & other) const
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
    if (this->robot_name != other.robot_name) {
      return false;
    }
    if (this->pose != other.pose) {
      return false;
    }
    if (this->velocity != other.velocity) {
      return false;
    }
    if (this->acceleration != other.acceleration) {
      return false;
    }
    if (this->stance_status != other.stance_status) {
      return false;
    }
    return true;
  }
  bool operator!=(const BaseState_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct BaseState_

// alias to use template instance with default allocator
using BaseState =
  dls2_interfaces::msg::BaseState_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace dls2_interfaces

#endif  // DLS2_INTERFACES__MSG__DETAIL__BASE_STATE__STRUCT_HPP_
