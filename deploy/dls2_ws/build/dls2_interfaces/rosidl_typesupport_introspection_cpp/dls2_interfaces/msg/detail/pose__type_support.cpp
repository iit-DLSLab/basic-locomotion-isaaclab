// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from dls2_interfaces:msg/Pose.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "dls2_interfaces/msg/detail/pose__struct.hpp"
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

void Pose_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) dls2_interfaces::msg::Pose(_init);
}

void Pose_fini_function(void * message_memory)
{
  auto typed_message = static_cast<dls2_interfaces::msg::Pose *>(message_memory);
  typed_message->~Pose();
}

size_t size_function__Pose__position(const void * untyped_member)
{
  (void)untyped_member;
  return 3;
}

const void * get_const_function__Pose__position(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::array<double, 3> *>(untyped_member);
  return &member[index];
}

void * get_function__Pose__position(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::array<double, 3> *>(untyped_member);
  return &member[index];
}

void fetch_function__Pose__position(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__Pose__position(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__Pose__position(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__Pose__position(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

size_t size_function__Pose__orientation(const void * untyped_member)
{
  (void)untyped_member;
  return 4;
}

const void * get_const_function__Pose__orientation(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::array<double, 4> *>(untyped_member);
  return &member[index];
}

void * get_function__Pose__orientation(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::array<double, 4> *>(untyped_member);
  return &member[index];
}

void fetch_function__Pose__orientation(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__Pose__orientation(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__Pose__orientation(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__Pose__orientation(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember Pose_message_member_array[2] = {
  {
    "position",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    3,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces::msg::Pose, position),  // bytes offset in struct
    nullptr,  // default value
    size_function__Pose__position,  // size() function pointer
    get_const_function__Pose__position,  // get_const(index) function pointer
    get_function__Pose__position,  // get(index) function pointer
    fetch_function__Pose__position,  // fetch(index, &value) function pointer
    assign_function__Pose__position,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "orientation",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    4,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces::msg::Pose, orientation),  // bytes offset in struct
    nullptr,  // default value
    size_function__Pose__orientation,  // size() function pointer
    get_const_function__Pose__orientation,  // get_const(index) function pointer
    get_function__Pose__orientation,  // get(index) function pointer
    fetch_function__Pose__orientation,  // fetch(index, &value) function pointer
    assign_function__Pose__orientation,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers Pose_message_members = {
  "dls2_interfaces::msg",  // message namespace
  "Pose",  // message name
  2,  // number of fields
  sizeof(dls2_interfaces::msg::Pose),
  Pose_message_member_array,  // message members
  Pose_init_function,  // function to initialize message memory (memory has to be allocated)
  Pose_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t Pose_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &Pose_message_members,
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
get_message_type_support_handle<dls2_interfaces::msg::Pose>()
{
  return &::dls2_interfaces::msg::rosidl_typesupport_introspection_cpp::Pose_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, dls2_interfaces, msg, Pose)() {
  return &::dls2_interfaces::msg::rosidl_typesupport_introspection_cpp::Pose_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
