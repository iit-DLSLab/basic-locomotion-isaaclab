// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from dls2_interfaces:msg/BlindState.idl
// generated code does not contain a copyright notice

#ifndef DLS2_INTERFACES__MSG__DETAIL__BLIND_STATE__STRUCT_HPP_
#define DLS2_INTERFACES__MSG__DETAIL__BLIND_STATE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__dls2_interfaces__msg__BlindState __attribute__((deprecated))
#else
# define DEPRECATED__dls2_interfaces__msg__BlindState __declspec(deprecated)
#endif

namespace dls2_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct BlindState_
{
  using Type = BlindState_<ContainerAllocator>;

  explicit BlindState_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
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

  explicit BlindState_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : frame_id(_alloc),
    robot_name(_alloc)
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
  using _joints_name_type =
    std::vector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>>;
  _joints_name_type joints_name;
  using _joints_position_type =
    std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>>;
  _joints_position_type joints_position;
  using _joints_velocity_type =
    std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>>;
  _joints_velocity_type joints_velocity;
  using _joints_acceleration_type =
    std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>>;
  _joints_acceleration_type joints_acceleration;
  using _joints_effort_type =
    std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>>;
  _joints_effort_type joints_effort;
  using _joints_temperature_type =
    std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>>;
  _joints_temperature_type joints_temperature;
  using _feet_contact_type =
    std::vector<bool, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<bool>>;
  _feet_contact_type feet_contact;
  using _current_feet_positions_type =
    std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>>;
  _current_feet_positions_type current_feet_positions;

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
  Type & set__joints_name(
    const std::vector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>> & _arg)
  {
    this->joints_name = _arg;
    return *this;
  }
  Type & set__joints_position(
    const std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>> & _arg)
  {
    this->joints_position = _arg;
    return *this;
  }
  Type & set__joints_velocity(
    const std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>> & _arg)
  {
    this->joints_velocity = _arg;
    return *this;
  }
  Type & set__joints_acceleration(
    const std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>> & _arg)
  {
    this->joints_acceleration = _arg;
    return *this;
  }
  Type & set__joints_effort(
    const std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>> & _arg)
  {
    this->joints_effort = _arg;
    return *this;
  }
  Type & set__joints_temperature(
    const std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>> & _arg)
  {
    this->joints_temperature = _arg;
    return *this;
  }
  Type & set__feet_contact(
    const std::vector<bool, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<bool>> & _arg)
  {
    this->feet_contact = _arg;
    return *this;
  }
  Type & set__current_feet_positions(
    const std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>> & _arg)
  {
    this->current_feet_positions = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    dls2_interfaces::msg::BlindState_<ContainerAllocator> *;
  using ConstRawPtr =
    const dls2_interfaces::msg::BlindState_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<dls2_interfaces::msg::BlindState_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<dls2_interfaces::msg::BlindState_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      dls2_interfaces::msg::BlindState_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<dls2_interfaces::msg::BlindState_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      dls2_interfaces::msg::BlindState_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<dls2_interfaces::msg::BlindState_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<dls2_interfaces::msg::BlindState_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<dls2_interfaces::msg::BlindState_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__dls2_interfaces__msg__BlindState
    std::shared_ptr<dls2_interfaces::msg::BlindState_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__dls2_interfaces__msg__BlindState
    std::shared_ptr<dls2_interfaces::msg::BlindState_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const BlindState_ & other) const
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
    if (this->joints_name != other.joints_name) {
      return false;
    }
    if (this->joints_position != other.joints_position) {
      return false;
    }
    if (this->joints_velocity != other.joints_velocity) {
      return false;
    }
    if (this->joints_acceleration != other.joints_acceleration) {
      return false;
    }
    if (this->joints_effort != other.joints_effort) {
      return false;
    }
    if (this->joints_temperature != other.joints_temperature) {
      return false;
    }
    if (this->feet_contact != other.feet_contact) {
      return false;
    }
    if (this->current_feet_positions != other.current_feet_positions) {
      return false;
    }
    return true;
  }
  bool operator!=(const BlindState_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct BlindState_

// alias to use template instance with default allocator
using BlindState =
  dls2_interfaces::msg::BlindState_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace dls2_interfaces

#endif  // DLS2_INTERFACES__MSG__DETAIL__BLIND_STATE__STRUCT_HPP_
