// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from dls2_interfaces:msg/DesiredTorques.idl
// generated code does not contain a copyright notice

#ifndef DLS2_INTERFACES__MSG__DETAIL__DESIRED_TORQUES__STRUCT_HPP_
#define DLS2_INTERFACES__MSG__DETAIL__DESIRED_TORQUES__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__dls2_interfaces__msg__DesiredTorques __attribute__((deprecated))
#else
# define DEPRECATED__dls2_interfaces__msg__DesiredTorques __declspec(deprecated)
#endif

namespace dls2_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct DesiredTorques_
{
  using Type = DesiredTorques_<ContainerAllocator>;

  explicit DesiredTorques_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->frame_id = "";
      this->sequence_id = 0ul;
      this->timestamp = 0.0;
    }
  }

  explicit DesiredTorques_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : frame_id(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->frame_id = "";
      this->sequence_id = 0ul;
      this->timestamp = 0.0;
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
  using _desired_torques_type =
    std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>>;
  _desired_torques_type desired_torques;

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
  Type & set__desired_torques(
    const std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>> & _arg)
  {
    this->desired_torques = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    dls2_interfaces::msg::DesiredTorques_<ContainerAllocator> *;
  using ConstRawPtr =
    const dls2_interfaces::msg::DesiredTorques_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<dls2_interfaces::msg::DesiredTorques_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<dls2_interfaces::msg::DesiredTorques_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      dls2_interfaces::msg::DesiredTorques_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<dls2_interfaces::msg::DesiredTorques_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      dls2_interfaces::msg::DesiredTorques_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<dls2_interfaces::msg::DesiredTorques_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<dls2_interfaces::msg::DesiredTorques_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<dls2_interfaces::msg::DesiredTorques_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__dls2_interfaces__msg__DesiredTorques
    std::shared_ptr<dls2_interfaces::msg::DesiredTorques_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__dls2_interfaces__msg__DesiredTorques
    std::shared_ptr<dls2_interfaces::msg::DesiredTorques_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const DesiredTorques_ & other) const
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
    if (this->desired_torques != other.desired_torques) {
      return false;
    }
    return true;
  }
  bool operator!=(const DesiredTorques_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct DesiredTorques_

// alias to use template instance with default allocator
using DesiredTorques =
  dls2_interfaces::msg::DesiredTorques_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace dls2_interfaces

#endif  // DLS2_INTERFACES__MSG__DETAIL__DESIRED_TORQUES__STRUCT_HPP_
