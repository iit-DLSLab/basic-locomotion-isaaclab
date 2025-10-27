// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from dls2_interfaces:msg/BlindState.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "dls2_interfaces/msg/detail/blind_state__struct.hpp"
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

void BlindState_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) dls2_interfaces::msg::BlindState(_init);
}

void BlindState_fini_function(void * message_memory)
{
  auto typed_message = static_cast<dls2_interfaces::msg::BlindState *>(message_memory);
  typed_message->~BlindState();
}

size_t size_function__BlindState__joints_name(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<std::string> *>(untyped_member);
  return member->size();
}

const void * get_const_function__BlindState__joints_name(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<std::string> *>(untyped_member);
  return &member[index];
}

void * get_function__BlindState__joints_name(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<std::string> *>(untyped_member);
  return &member[index];
}

void fetch_function__BlindState__joints_name(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const std::string *>(
    get_const_function__BlindState__joints_name(untyped_member, index));
  auto & value = *reinterpret_cast<std::string *>(untyped_value);
  value = item;
}

void assign_function__BlindState__joints_name(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<std::string *>(
    get_function__BlindState__joints_name(untyped_member, index));
  const auto & value = *reinterpret_cast<const std::string *>(untyped_value);
  item = value;
}

void resize_function__BlindState__joints_name(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<std::string> *>(untyped_member);
  member->resize(size);
}

size_t size_function__BlindState__joints_position(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<double> *>(untyped_member);
  return member->size();
}

const void * get_const_function__BlindState__joints_position(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<double> *>(untyped_member);
  return &member[index];
}

void * get_function__BlindState__joints_position(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<double> *>(untyped_member);
  return &member[index];
}

void fetch_function__BlindState__joints_position(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__BlindState__joints_position(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__BlindState__joints_position(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__BlindState__joints_position(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

void resize_function__BlindState__joints_position(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<double> *>(untyped_member);
  member->resize(size);
}

size_t size_function__BlindState__joints_velocity(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<double> *>(untyped_member);
  return member->size();
}

const void * get_const_function__BlindState__joints_velocity(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<double> *>(untyped_member);
  return &member[index];
}

void * get_function__BlindState__joints_velocity(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<double> *>(untyped_member);
  return &member[index];
}

void fetch_function__BlindState__joints_velocity(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__BlindState__joints_velocity(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__BlindState__joints_velocity(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__BlindState__joints_velocity(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

void resize_function__BlindState__joints_velocity(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<double> *>(untyped_member);
  member->resize(size);
}

size_t size_function__BlindState__joints_acceleration(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<double> *>(untyped_member);
  return member->size();
}

const void * get_const_function__BlindState__joints_acceleration(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<double> *>(untyped_member);
  return &member[index];
}

void * get_function__BlindState__joints_acceleration(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<double> *>(untyped_member);
  return &member[index];
}

void fetch_function__BlindState__joints_acceleration(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__BlindState__joints_acceleration(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__BlindState__joints_acceleration(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__BlindState__joints_acceleration(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

void resize_function__BlindState__joints_acceleration(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<double> *>(untyped_member);
  member->resize(size);
}

size_t size_function__BlindState__joints_effort(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<double> *>(untyped_member);
  return member->size();
}

const void * get_const_function__BlindState__joints_effort(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<double> *>(untyped_member);
  return &member[index];
}

void * get_function__BlindState__joints_effort(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<double> *>(untyped_member);
  return &member[index];
}

void fetch_function__BlindState__joints_effort(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__BlindState__joints_effort(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__BlindState__joints_effort(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__BlindState__joints_effort(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

void resize_function__BlindState__joints_effort(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<double> *>(untyped_member);
  member->resize(size);
}

size_t size_function__BlindState__joints_temperature(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<double> *>(untyped_member);
  return member->size();
}

const void * get_const_function__BlindState__joints_temperature(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<double> *>(untyped_member);
  return &member[index];
}

void * get_function__BlindState__joints_temperature(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<double> *>(untyped_member);
  return &member[index];
}

void fetch_function__BlindState__joints_temperature(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__BlindState__joints_temperature(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__BlindState__joints_temperature(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__BlindState__joints_temperature(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

void resize_function__BlindState__joints_temperature(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<double> *>(untyped_member);
  member->resize(size);
}

size_t size_function__BlindState__feet_contact(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<bool> *>(untyped_member);
  return member->size();
}

void fetch_function__BlindState__feet_contact(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & member = *reinterpret_cast<const std::vector<bool> *>(untyped_member);
  auto & value = *reinterpret_cast<bool *>(untyped_value);
  value = member[index];
}

void assign_function__BlindState__feet_contact(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & member = *reinterpret_cast<std::vector<bool> *>(untyped_member);
  const auto & value = *reinterpret_cast<const bool *>(untyped_value);
  member[index] = value;
}

void resize_function__BlindState__feet_contact(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<bool> *>(untyped_member);
  member->resize(size);
}

size_t size_function__BlindState__current_feet_positions(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<double> *>(untyped_member);
  return member->size();
}

const void * get_const_function__BlindState__current_feet_positions(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<double> *>(untyped_member);
  return &member[index];
}

void * get_function__BlindState__current_feet_positions(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<double> *>(untyped_member);
  return &member[index];
}

void fetch_function__BlindState__current_feet_positions(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__BlindState__current_feet_positions(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__BlindState__current_feet_positions(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__BlindState__current_feet_positions(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

void resize_function__BlindState__current_feet_positions(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<double> *>(untyped_member);
  member->resize(size);
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember BlindState_message_member_array[12] = {
  {
    "frame_id",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces::msg::BlindState, frame_id),  // bytes offset in struct
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
    offsetof(dls2_interfaces::msg::BlindState, sequence_id),  // bytes offset in struct
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
    offsetof(dls2_interfaces::msg::BlindState, timestamp),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "robot_name",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces::msg::BlindState, robot_name),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "joints_name",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces::msg::BlindState, joints_name),  // bytes offset in struct
    nullptr,  // default value
    size_function__BlindState__joints_name,  // size() function pointer
    get_const_function__BlindState__joints_name,  // get_const(index) function pointer
    get_function__BlindState__joints_name,  // get(index) function pointer
    fetch_function__BlindState__joints_name,  // fetch(index, &value) function pointer
    assign_function__BlindState__joints_name,  // assign(index, value) function pointer
    resize_function__BlindState__joints_name  // resize(index) function pointer
  },
  {
    "joints_position",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces::msg::BlindState, joints_position),  // bytes offset in struct
    nullptr,  // default value
    size_function__BlindState__joints_position,  // size() function pointer
    get_const_function__BlindState__joints_position,  // get_const(index) function pointer
    get_function__BlindState__joints_position,  // get(index) function pointer
    fetch_function__BlindState__joints_position,  // fetch(index, &value) function pointer
    assign_function__BlindState__joints_position,  // assign(index, value) function pointer
    resize_function__BlindState__joints_position  // resize(index) function pointer
  },
  {
    "joints_velocity",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces::msg::BlindState, joints_velocity),  // bytes offset in struct
    nullptr,  // default value
    size_function__BlindState__joints_velocity,  // size() function pointer
    get_const_function__BlindState__joints_velocity,  // get_const(index) function pointer
    get_function__BlindState__joints_velocity,  // get(index) function pointer
    fetch_function__BlindState__joints_velocity,  // fetch(index, &value) function pointer
    assign_function__BlindState__joints_velocity,  // assign(index, value) function pointer
    resize_function__BlindState__joints_velocity  // resize(index) function pointer
  },
  {
    "joints_acceleration",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces::msg::BlindState, joints_acceleration),  // bytes offset in struct
    nullptr,  // default value
    size_function__BlindState__joints_acceleration,  // size() function pointer
    get_const_function__BlindState__joints_acceleration,  // get_const(index) function pointer
    get_function__BlindState__joints_acceleration,  // get(index) function pointer
    fetch_function__BlindState__joints_acceleration,  // fetch(index, &value) function pointer
    assign_function__BlindState__joints_acceleration,  // assign(index, value) function pointer
    resize_function__BlindState__joints_acceleration  // resize(index) function pointer
  },
  {
    "joints_effort",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces::msg::BlindState, joints_effort),  // bytes offset in struct
    nullptr,  // default value
    size_function__BlindState__joints_effort,  // size() function pointer
    get_const_function__BlindState__joints_effort,  // get_const(index) function pointer
    get_function__BlindState__joints_effort,  // get(index) function pointer
    fetch_function__BlindState__joints_effort,  // fetch(index, &value) function pointer
    assign_function__BlindState__joints_effort,  // assign(index, value) function pointer
    resize_function__BlindState__joints_effort  // resize(index) function pointer
  },
  {
    "joints_temperature",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces::msg::BlindState, joints_temperature),  // bytes offset in struct
    nullptr,  // default value
    size_function__BlindState__joints_temperature,  // size() function pointer
    get_const_function__BlindState__joints_temperature,  // get_const(index) function pointer
    get_function__BlindState__joints_temperature,  // get(index) function pointer
    fetch_function__BlindState__joints_temperature,  // fetch(index, &value) function pointer
    assign_function__BlindState__joints_temperature,  // assign(index, value) function pointer
    resize_function__BlindState__joints_temperature  // resize(index) function pointer
  },
  {
    "feet_contact",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces::msg::BlindState, feet_contact),  // bytes offset in struct
    nullptr,  // default value
    size_function__BlindState__feet_contact,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    fetch_function__BlindState__feet_contact,  // fetch(index, &value) function pointer
    assign_function__BlindState__feet_contact,  // assign(index, value) function pointer
    resize_function__BlindState__feet_contact  // resize(index) function pointer
  },
  {
    "current_feet_positions",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces::msg::BlindState, current_feet_positions),  // bytes offset in struct
    nullptr,  // default value
    size_function__BlindState__current_feet_positions,  // size() function pointer
    get_const_function__BlindState__current_feet_positions,  // get_const(index) function pointer
    get_function__BlindState__current_feet_positions,  // get(index) function pointer
    fetch_function__BlindState__current_feet_positions,  // fetch(index, &value) function pointer
    assign_function__BlindState__current_feet_positions,  // assign(index, value) function pointer
    resize_function__BlindState__current_feet_positions  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers BlindState_message_members = {
  "dls2_interfaces::msg",  // message namespace
  "BlindState",  // message name
  12,  // number of fields
  sizeof(dls2_interfaces::msg::BlindState),
  BlindState_message_member_array,  // message members
  BlindState_init_function,  // function to initialize message memory (memory has to be allocated)
  BlindState_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t BlindState_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &BlindState_message_members,
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
get_message_type_support_handle<dls2_interfaces::msg::BlindState>()
{
  return &::dls2_interfaces::msg::rosidl_typesupport_introspection_cpp::BlindState_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, dls2_interfaces, msg, BlindState)() {
  return &::dls2_interfaces::msg::rosidl_typesupport_introspection_cpp::BlindState_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
