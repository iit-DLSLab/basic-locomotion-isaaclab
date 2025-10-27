// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from dls2_interfaces:msg/TrajectoryGenerator.idl
// generated code does not contain a copyright notice

#ifndef DLS2_INTERFACES__MSG__DETAIL__TRAJECTORY_GENERATOR__STRUCT_HPP_
#define DLS2_INTERFACES__MSG__DETAIL__TRAJECTORY_GENERATOR__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'com_pose'
#include "dls2_interfaces/msg/detail/pose__struct.hpp"
// Member 'com_vel'
// Member 'com_acc'
#include "dls2_interfaces/msg/detail/screw__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__dls2_interfaces__msg__TrajectoryGenerator __attribute__((deprecated))
#else
# define DEPRECATED__dls2_interfaces__msg__TrajectoryGenerator __declspec(deprecated)
#endif

namespace dls2_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct TrajectoryGenerator_
{
  using Type = TrajectoryGenerator_<ContainerAllocator>;

  explicit TrajectoryGenerator_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : com_pose(_init),
    com_vel(_init),
    com_acc(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->frame_id = "";
      this->sequence_id = 0ul;
      this->timestamp = 0.0;
      std::fill<typename std::array<double, 6>::iterator, double>(this->wrench.begin(), this->wrench.end(), 0.0);
    }
  }

  explicit TrajectoryGenerator_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : frame_id(_alloc),
    com_pose(_alloc, _init),
    com_vel(_alloc, _init),
    com_acc(_alloc, _init),
    wrench(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->frame_id = "";
      this->sequence_id = 0ul;
      this->timestamp = 0.0;
      std::fill<typename std::array<double, 6>::iterator, double>(this->wrench.begin(), this->wrench.end(), 0.0);
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
  using _com_pose_type =
    dls2_interfaces::msg::Pose_<ContainerAllocator>;
  _com_pose_type com_pose;
  using _com_vel_type =
    dls2_interfaces::msg::Screw_<ContainerAllocator>;
  _com_vel_type com_vel;
  using _com_acc_type =
    dls2_interfaces::msg::Screw_<ContainerAllocator>;
  _com_acc_type com_acc;
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
  using _kp_type =
    std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>>;
  _kp_type kp;
  using _kd_type =
    std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>>;
  _kd_type kd;
  using _wrench_type =
    std::array<double, 6>;
  _wrench_type wrench;
  using _stance_legs_type =
    std::vector<bool, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<bool>>;
  _stance_legs_type stance_legs;
  using _nominal_touch_down_type =
    std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>>;
  _nominal_touch_down_type nominal_touch_down;
  using _touch_down_type =
    std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>>;
  _touch_down_type touch_down;
  using _swing_period_type =
    std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>>;
  _swing_period_type swing_period;
  using _normal_force_max_type =
    std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>>;
  _normal_force_max_type normal_force_max;
  using _normal_force_min_type =
    std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>>;
  _normal_force_min_type normal_force_min;

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
  Type & set__com_pose(
    const dls2_interfaces::msg::Pose_<ContainerAllocator> & _arg)
  {
    this->com_pose = _arg;
    return *this;
  }
  Type & set__com_vel(
    const dls2_interfaces::msg::Screw_<ContainerAllocator> & _arg)
  {
    this->com_vel = _arg;
    return *this;
  }
  Type & set__com_acc(
    const dls2_interfaces::msg::Screw_<ContainerAllocator> & _arg)
  {
    this->com_acc = _arg;
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
  Type & set__kp(
    const std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>> & _arg)
  {
    this->kp = _arg;
    return *this;
  }
  Type & set__kd(
    const std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>> & _arg)
  {
    this->kd = _arg;
    return *this;
  }
  Type & set__wrench(
    const std::array<double, 6> & _arg)
  {
    this->wrench = _arg;
    return *this;
  }
  Type & set__stance_legs(
    const std::vector<bool, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<bool>> & _arg)
  {
    this->stance_legs = _arg;
    return *this;
  }
  Type & set__nominal_touch_down(
    const std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>> & _arg)
  {
    this->nominal_touch_down = _arg;
    return *this;
  }
  Type & set__touch_down(
    const std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>> & _arg)
  {
    this->touch_down = _arg;
    return *this;
  }
  Type & set__swing_period(
    const std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>> & _arg)
  {
    this->swing_period = _arg;
    return *this;
  }
  Type & set__normal_force_max(
    const std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>> & _arg)
  {
    this->normal_force_max = _arg;
    return *this;
  }
  Type & set__normal_force_min(
    const std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>> & _arg)
  {
    this->normal_force_min = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    dls2_interfaces::msg::TrajectoryGenerator_<ContainerAllocator> *;
  using ConstRawPtr =
    const dls2_interfaces::msg::TrajectoryGenerator_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<dls2_interfaces::msg::TrajectoryGenerator_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<dls2_interfaces::msg::TrajectoryGenerator_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      dls2_interfaces::msg::TrajectoryGenerator_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<dls2_interfaces::msg::TrajectoryGenerator_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      dls2_interfaces::msg::TrajectoryGenerator_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<dls2_interfaces::msg::TrajectoryGenerator_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<dls2_interfaces::msg::TrajectoryGenerator_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<dls2_interfaces::msg::TrajectoryGenerator_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__dls2_interfaces__msg__TrajectoryGenerator
    std::shared_ptr<dls2_interfaces::msg::TrajectoryGenerator_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__dls2_interfaces__msg__TrajectoryGenerator
    std::shared_ptr<dls2_interfaces::msg::TrajectoryGenerator_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const TrajectoryGenerator_ & other) const
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
    if (this->com_pose != other.com_pose) {
      return false;
    }
    if (this->com_vel != other.com_vel) {
      return false;
    }
    if (this->com_acc != other.com_acc) {
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
    if (this->kp != other.kp) {
      return false;
    }
    if (this->kd != other.kd) {
      return false;
    }
    if (this->wrench != other.wrench) {
      return false;
    }
    if (this->stance_legs != other.stance_legs) {
      return false;
    }
    if (this->nominal_touch_down != other.nominal_touch_down) {
      return false;
    }
    if (this->touch_down != other.touch_down) {
      return false;
    }
    if (this->swing_period != other.swing_period) {
      return false;
    }
    if (this->normal_force_max != other.normal_force_max) {
      return false;
    }
    if (this->normal_force_min != other.normal_force_min) {
      return false;
    }
    return true;
  }
  bool operator!=(const TrajectoryGenerator_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct TrajectoryGenerator_

// alias to use template instance with default allocator
using TrajectoryGenerator =
  dls2_interfaces::msg::TrajectoryGenerator_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace dls2_interfaces

#endif  // DLS2_INTERFACES__MSG__DETAIL__TRAJECTORY_GENERATOR__STRUCT_HPP_
