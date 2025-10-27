// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from dls2_interfaces:msg/TrajectoryGenerator.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "dls2_interfaces/msg/detail/trajectory_generator__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace dls2_interfaces
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void TrajectoryGenerator_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) dls2_interfaces::msg::TrajectoryGenerator(_init);
}

void TrajectoryGenerator_fini_function(void * message_memory)
{
  auto typed_message = static_cast<dls2_interfaces::msg::TrajectoryGenerator *>(message_memory);
  typed_message->~TrajectoryGenerator();
}

size_t size_function__TrajectoryGenerator__joints_position(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<double> *>(untyped_member);
  return member->size();
}

const void * get_const_function__TrajectoryGenerator__joints_position(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<double> *>(untyped_member);
  return &member[index];
}

void * get_function__TrajectoryGenerator__joints_position(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<double> *>(untyped_member);
  return &member[index];
}

void fetch_function__TrajectoryGenerator__joints_position(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__TrajectoryGenerator__joints_position(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__TrajectoryGenerator__joints_position(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__TrajectoryGenerator__joints_position(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

void resize_function__TrajectoryGenerator__joints_position(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<double> *>(untyped_member);
  member->resize(size);
}

size_t size_function__TrajectoryGenerator__joints_velocity(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<double> *>(untyped_member);
  return member->size();
}

const void * get_const_function__TrajectoryGenerator__joints_velocity(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<double> *>(untyped_member);
  return &member[index];
}

void * get_function__TrajectoryGenerator__joints_velocity(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<double> *>(untyped_member);
  return &member[index];
}

void fetch_function__TrajectoryGenerator__joints_velocity(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__TrajectoryGenerator__joints_velocity(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__TrajectoryGenerator__joints_velocity(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__TrajectoryGenerator__joints_velocity(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

void resize_function__TrajectoryGenerator__joints_velocity(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<double> *>(untyped_member);
  member->resize(size);
}

size_t size_function__TrajectoryGenerator__joints_acceleration(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<double> *>(untyped_member);
  return member->size();
}

const void * get_const_function__TrajectoryGenerator__joints_acceleration(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<double> *>(untyped_member);
  return &member[index];
}

void * get_function__TrajectoryGenerator__joints_acceleration(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<double> *>(untyped_member);
  return &member[index];
}

void fetch_function__TrajectoryGenerator__joints_acceleration(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__TrajectoryGenerator__joints_acceleration(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__TrajectoryGenerator__joints_acceleration(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__TrajectoryGenerator__joints_acceleration(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

void resize_function__TrajectoryGenerator__joints_acceleration(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<double> *>(untyped_member);
  member->resize(size);
}

size_t size_function__TrajectoryGenerator__joints_effort(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<double> *>(untyped_member);
  return member->size();
}

const void * get_const_function__TrajectoryGenerator__joints_effort(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<double> *>(untyped_member);
  return &member[index];
}

void * get_function__TrajectoryGenerator__joints_effort(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<double> *>(untyped_member);
  return &member[index];
}

void fetch_function__TrajectoryGenerator__joints_effort(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__TrajectoryGenerator__joints_effort(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__TrajectoryGenerator__joints_effort(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__TrajectoryGenerator__joints_effort(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

void resize_function__TrajectoryGenerator__joints_effort(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<double> *>(untyped_member);
  member->resize(size);
}

size_t size_function__TrajectoryGenerator__kp(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<double> *>(untyped_member);
  return member->size();
}

const void * get_const_function__TrajectoryGenerator__kp(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<double> *>(untyped_member);
  return &member[index];
}

void * get_function__TrajectoryGenerator__kp(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<double> *>(untyped_member);
  return &member[index];
}

void fetch_function__TrajectoryGenerator__kp(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__TrajectoryGenerator__kp(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__TrajectoryGenerator__kp(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__TrajectoryGenerator__kp(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

void resize_function__TrajectoryGenerator__kp(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<double> *>(untyped_member);
  member->resize(size);
}

size_t size_function__TrajectoryGenerator__kd(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<double> *>(untyped_member);
  return member->size();
}

const void * get_const_function__TrajectoryGenerator__kd(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<double> *>(untyped_member);
  return &member[index];
}

void * get_function__TrajectoryGenerator__kd(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<double> *>(untyped_member);
  return &member[index];
}

void fetch_function__TrajectoryGenerator__kd(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__TrajectoryGenerator__kd(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__TrajectoryGenerator__kd(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__TrajectoryGenerator__kd(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

void resize_function__TrajectoryGenerator__kd(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<double> *>(untyped_member);
  member->resize(size);
}

size_t size_function__TrajectoryGenerator__wrench(const void * untyped_member)
{
  (void)untyped_member;
  return 6;
}

const void * get_const_function__TrajectoryGenerator__wrench(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::array<double, 6> *>(untyped_member);
  return &member[index];
}

void * get_function__TrajectoryGenerator__wrench(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::array<double, 6> *>(untyped_member);
  return &member[index];
}

void fetch_function__TrajectoryGenerator__wrench(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__TrajectoryGenerator__wrench(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__TrajectoryGenerator__wrench(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__TrajectoryGenerator__wrench(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

size_t size_function__TrajectoryGenerator__stance_legs(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<bool> *>(untyped_member);
  return member->size();
}

void fetch_function__TrajectoryGenerator__stance_legs(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & member = *reinterpret_cast<const std::vector<bool> *>(untyped_member);
  auto & value = *reinterpret_cast<bool *>(untyped_value);
  value = member[index];
}

void assign_function__TrajectoryGenerator__stance_legs(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & member = *reinterpret_cast<std::vector<bool> *>(untyped_member);
  const auto & value = *reinterpret_cast<const bool *>(untyped_value);
  member[index] = value;
}

void resize_function__TrajectoryGenerator__stance_legs(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<bool> *>(untyped_member);
  member->resize(size);
}

size_t size_function__TrajectoryGenerator__nominal_touch_down(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<double> *>(untyped_member);
  return member->size();
}

const void * get_const_function__TrajectoryGenerator__nominal_touch_down(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<double> *>(untyped_member);
  return &member[index];
}

void * get_function__TrajectoryGenerator__nominal_touch_down(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<double> *>(untyped_member);
  return &member[index];
}

void fetch_function__TrajectoryGenerator__nominal_touch_down(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__TrajectoryGenerator__nominal_touch_down(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__TrajectoryGenerator__nominal_touch_down(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__TrajectoryGenerator__nominal_touch_down(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

void resize_function__TrajectoryGenerator__nominal_touch_down(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<double> *>(untyped_member);
  member->resize(size);
}

size_t size_function__TrajectoryGenerator__touch_down(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<double> *>(untyped_member);
  return member->size();
}

const void * get_const_function__TrajectoryGenerator__touch_down(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<double> *>(untyped_member);
  return &member[index];
}

void * get_function__TrajectoryGenerator__touch_down(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<double> *>(untyped_member);
  return &member[index];
}

void fetch_function__TrajectoryGenerator__touch_down(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__TrajectoryGenerator__touch_down(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__TrajectoryGenerator__touch_down(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__TrajectoryGenerator__touch_down(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

void resize_function__TrajectoryGenerator__touch_down(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<double> *>(untyped_member);
  member->resize(size);
}

size_t size_function__TrajectoryGenerator__swing_period(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<double> *>(untyped_member);
  return member->size();
}

const void * get_const_function__TrajectoryGenerator__swing_period(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<double> *>(untyped_member);
  return &member[index];
}

void * get_function__TrajectoryGenerator__swing_period(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<double> *>(untyped_member);
  return &member[index];
}

void fetch_function__TrajectoryGenerator__swing_period(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__TrajectoryGenerator__swing_period(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__TrajectoryGenerator__swing_period(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__TrajectoryGenerator__swing_period(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

void resize_function__TrajectoryGenerator__swing_period(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<double> *>(untyped_member);
  member->resize(size);
}

size_t size_function__TrajectoryGenerator__normal_force_max(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<double> *>(untyped_member);
  return member->size();
}

const void * get_const_function__TrajectoryGenerator__normal_force_max(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<double> *>(untyped_member);
  return &member[index];
}

void * get_function__TrajectoryGenerator__normal_force_max(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<double> *>(untyped_member);
  return &member[index];
}

void fetch_function__TrajectoryGenerator__normal_force_max(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__TrajectoryGenerator__normal_force_max(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__TrajectoryGenerator__normal_force_max(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__TrajectoryGenerator__normal_force_max(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

void resize_function__TrajectoryGenerator__normal_force_max(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<double> *>(untyped_member);
  member->resize(size);
}

size_t size_function__TrajectoryGenerator__normal_force_min(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<double> *>(untyped_member);
  return member->size();
}

const void * get_const_function__TrajectoryGenerator__normal_force_min(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<double> *>(untyped_member);
  return &member[index];
}

void * get_function__TrajectoryGenerator__normal_force_min(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<double> *>(untyped_member);
  return &member[index];
}

void fetch_function__TrajectoryGenerator__normal_force_min(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__TrajectoryGenerator__normal_force_min(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__TrajectoryGenerator__normal_force_min(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__TrajectoryGenerator__normal_force_min(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

void resize_function__TrajectoryGenerator__normal_force_min(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<double> *>(untyped_member);
  member->resize(size);
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember TrajectoryGenerator_message_member_array[19] = {
  {
    "frame_id",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces::msg::TrajectoryGenerator, frame_id),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "sequence_id",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_UINT32,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces::msg::TrajectoryGenerator, sequence_id),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "timestamp",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces::msg::TrajectoryGenerator, timestamp),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "com_pose",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<dls2_interfaces::msg::Pose>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces::msg::TrajectoryGenerator, com_pose),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "com_vel",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<dls2_interfaces::msg::Screw>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces::msg::TrajectoryGenerator, com_vel),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "com_acc",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<dls2_interfaces::msg::Screw>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces::msg::TrajectoryGenerator, com_acc),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "joints_position",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces::msg::TrajectoryGenerator, joints_position),  // bytes offset in struct
    nullptr,  // default value
    size_function__TrajectoryGenerator__joints_position,  // size() function pointer
    get_const_function__TrajectoryGenerator__joints_position,  // get_const(index) function pointer
    get_function__TrajectoryGenerator__joints_position,  // get(index) function pointer
    fetch_function__TrajectoryGenerator__joints_position,  // fetch(index, &value) function pointer
    assign_function__TrajectoryGenerator__joints_position,  // assign(index, value) function pointer
    resize_function__TrajectoryGenerator__joints_position  // resize(index) function pointer
  },
  {
    "joints_velocity",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces::msg::TrajectoryGenerator, joints_velocity),  // bytes offset in struct
    nullptr,  // default value
    size_function__TrajectoryGenerator__joints_velocity,  // size() function pointer
    get_const_function__TrajectoryGenerator__joints_velocity,  // get_const(index) function pointer
    get_function__TrajectoryGenerator__joints_velocity,  // get(index) function pointer
    fetch_function__TrajectoryGenerator__joints_velocity,  // fetch(index, &value) function pointer
    assign_function__TrajectoryGenerator__joints_velocity,  // assign(index, value) function pointer
    resize_function__TrajectoryGenerator__joints_velocity  // resize(index) function pointer
  },
  {
    "joints_acceleration",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces::msg::TrajectoryGenerator, joints_acceleration),  // bytes offset in struct
    nullptr,  // default value
    size_function__TrajectoryGenerator__joints_acceleration,  // size() function pointer
    get_const_function__TrajectoryGenerator__joints_acceleration,  // get_const(index) function pointer
    get_function__TrajectoryGenerator__joints_acceleration,  // get(index) function pointer
    fetch_function__TrajectoryGenerator__joints_acceleration,  // fetch(index, &value) function pointer
    assign_function__TrajectoryGenerator__joints_acceleration,  // assign(index, value) function pointer
    resize_function__TrajectoryGenerator__joints_acceleration  // resize(index) function pointer
  },
  {
    "joints_effort",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces::msg::TrajectoryGenerator, joints_effort),  // bytes offset in struct
    nullptr,  // default value
    size_function__TrajectoryGenerator__joints_effort,  // size() function pointer
    get_const_function__TrajectoryGenerator__joints_effort,  // get_const(index) function pointer
    get_function__TrajectoryGenerator__joints_effort,  // get(index) function pointer
    fetch_function__TrajectoryGenerator__joints_effort,  // fetch(index, &value) function pointer
    assign_function__TrajectoryGenerator__joints_effort,  // assign(index, value) function pointer
    resize_function__TrajectoryGenerator__joints_effort  // resize(index) function pointer
  },
  {
    "kp",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces::msg::TrajectoryGenerator, kp),  // bytes offset in struct
    nullptr,  // default value
    size_function__TrajectoryGenerator__kp,  // size() function pointer
    get_const_function__TrajectoryGenerator__kp,  // get_const(index) function pointer
    get_function__TrajectoryGenerator__kp,  // get(index) function pointer
    fetch_function__TrajectoryGenerator__kp,  // fetch(index, &value) function pointer
    assign_function__TrajectoryGenerator__kp,  // assign(index, value) function pointer
    resize_function__TrajectoryGenerator__kp  // resize(index) function pointer
  },
  {
    "kd",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces::msg::TrajectoryGenerator, kd),  // bytes offset in struct
    nullptr,  // default value
    size_function__TrajectoryGenerator__kd,  // size() function pointer
    get_const_function__TrajectoryGenerator__kd,  // get_const(index) function pointer
    get_function__TrajectoryGenerator__kd,  // get(index) function pointer
    fetch_function__TrajectoryGenerator__kd,  // fetch(index, &value) function pointer
    assign_function__TrajectoryGenerator__kd,  // assign(index, value) function pointer
    resize_function__TrajectoryGenerator__kd  // resize(index) function pointer
  },
  {
    "wrench",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    6,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces::msg::TrajectoryGenerator, wrench),  // bytes offset in struct
    nullptr,  // default value
    size_function__TrajectoryGenerator__wrench,  // size() function pointer
    get_const_function__TrajectoryGenerator__wrench,  // get_const(index) function pointer
    get_function__TrajectoryGenerator__wrench,  // get(index) function pointer
    fetch_function__TrajectoryGenerator__wrench,  // fetch(index, &value) function pointer
    assign_function__TrajectoryGenerator__wrench,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "stance_legs",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces::msg::TrajectoryGenerator, stance_legs),  // bytes offset in struct
    nullptr,  // default value
    size_function__TrajectoryGenerator__stance_legs,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    fetch_function__TrajectoryGenerator__stance_legs,  // fetch(index, &value) function pointer
    assign_function__TrajectoryGenerator__stance_legs,  // assign(index, value) function pointer
    resize_function__TrajectoryGenerator__stance_legs  // resize(index) function pointer
  },
  {
    "nominal_touch_down",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces::msg::TrajectoryGenerator, nominal_touch_down),  // bytes offset in struct
    nullptr,  // default value
    size_function__TrajectoryGenerator__nominal_touch_down,  // size() function pointer
    get_const_function__TrajectoryGenerator__nominal_touch_down,  // get_const(index) function pointer
    get_function__TrajectoryGenerator__nominal_touch_down,  // get(index) function pointer
    fetch_function__TrajectoryGenerator__nominal_touch_down,  // fetch(index, &value) function pointer
    assign_function__TrajectoryGenerator__nominal_touch_down,  // assign(index, value) function pointer
    resize_function__TrajectoryGenerator__nominal_touch_down  // resize(index) function pointer
  },
  {
    "touch_down",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces::msg::TrajectoryGenerator, touch_down),  // bytes offset in struct
    nullptr,  // default value
    size_function__TrajectoryGenerator__touch_down,  // size() function pointer
    get_const_function__TrajectoryGenerator__touch_down,  // get_const(index) function pointer
    get_function__TrajectoryGenerator__touch_down,  // get(index) function pointer
    fetch_function__TrajectoryGenerator__touch_down,  // fetch(index, &value) function pointer
    assign_function__TrajectoryGenerator__touch_down,  // assign(index, value) function pointer
    resize_function__TrajectoryGenerator__touch_down  // resize(index) function pointer
  },
  {
    "swing_period",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces::msg::TrajectoryGenerator, swing_period),  // bytes offset in struct
    nullptr,  // default value
    size_function__TrajectoryGenerator__swing_period,  // size() function pointer
    get_const_function__TrajectoryGenerator__swing_period,  // get_const(index) function pointer
    get_function__TrajectoryGenerator__swing_period,  // get(index) function pointer
    fetch_function__TrajectoryGenerator__swing_period,  // fetch(index, &value) function pointer
    assign_function__TrajectoryGenerator__swing_period,  // assign(index, value) function pointer
    resize_function__TrajectoryGenerator__swing_period  // resize(index) function pointer
  },
  {
    "normal_force_max",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces::msg::TrajectoryGenerator, normal_force_max),  // bytes offset in struct
    nullptr,  // default value
    size_function__TrajectoryGenerator__normal_force_max,  // size() function pointer
    get_const_function__TrajectoryGenerator__normal_force_max,  // get_const(index) function pointer
    get_function__TrajectoryGenerator__normal_force_max,  // get(index) function pointer
    fetch_function__TrajectoryGenerator__normal_force_max,  // fetch(index, &value) function pointer
    assign_function__TrajectoryGenerator__normal_force_max,  // assign(index, value) function pointer
    resize_function__TrajectoryGenerator__normal_force_max  // resize(index) function pointer
  },
  {
    "normal_force_min",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces::msg::TrajectoryGenerator, normal_force_min),  // bytes offset in struct
    nullptr,  // default value
    size_function__TrajectoryGenerator__normal_force_min,  // size() function pointer
    get_const_function__TrajectoryGenerator__normal_force_min,  // get_const(index) function pointer
    get_function__TrajectoryGenerator__normal_force_min,  // get(index) function pointer
    fetch_function__TrajectoryGenerator__normal_force_min,  // fetch(index, &value) function pointer
    assign_function__TrajectoryGenerator__normal_force_min,  // assign(index, value) function pointer
    resize_function__TrajectoryGenerator__normal_force_min  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers TrajectoryGenerator_message_members = {
  "dls2_interfaces::msg",  // message namespace
  "TrajectoryGenerator",  // message name
  19,  // number of fields
  sizeof(dls2_interfaces::msg::TrajectoryGenerator),
  TrajectoryGenerator_message_member_array,  // message members
  TrajectoryGenerator_init_function,  // function to initialize message memory (memory has to be allocated)
  TrajectoryGenerator_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t TrajectoryGenerator_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &TrajectoryGenerator_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace dls2_interfaces


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<dls2_interfaces::msg::TrajectoryGenerator>()
{
  return &::dls2_interfaces::msg::rosidl_typesupport_introspection_cpp::TrajectoryGenerator_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, dls2_interfaces, msg, TrajectoryGenerator)() {
  return &::dls2_interfaces::msg::rosidl_typesupport_introspection_cpp::TrajectoryGenerator_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
