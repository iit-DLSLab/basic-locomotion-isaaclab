// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from dls2_interfaces:msg/Screw.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "dls2_interfaces/msg/detail/screw__struct.hpp"
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

void Screw_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) dls2_interfaces::msg::Screw(_init);
}

void Screw_fini_function(void * message_memory)
{
  auto typed_message = static_cast<dls2_interfaces::msg::Screw *>(message_memory);
  typed_message->~Screw();
}

size_t size_function__Screw__linear(const void * untyped_member)
{
  (void)untyped_member;
  return 3;
}

const void * get_const_function__Screw__linear(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::array<double, 3> *>(untyped_member);
  return &member[index];
}

void * get_function__Screw__linear(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::array<double, 3> *>(untyped_member);
  return &member[index];
}

void fetch_function__Screw__linear(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__Screw__linear(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__Screw__linear(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__Screw__linear(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

size_t size_function__Screw__angular(const void * untyped_member)
{
  (void)untyped_member;
  return 3;
}

const void * get_const_function__Screw__angular(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::array<double, 3> *>(untyped_member);
  return &member[index];
}

void * get_function__Screw__angular(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::array<double, 3> *>(untyped_member);
  return &member[index];
}

void fetch_function__Screw__angular(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__Screw__angular(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__Screw__angular(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__Screw__angular(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember Screw_message_member_array[2] = {
  {
    "linear",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    3,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces::msg::Screw, linear),  // bytes offset in struct
    nullptr,  // default value
    size_function__Screw__linear,  // size() function pointer
    get_const_function__Screw__linear,  // get_const(index) function pointer
    get_function__Screw__linear,  // get(index) function pointer
    fetch_function__Screw__linear,  // fetch(index, &value) function pointer
    assign_function__Screw__linear,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "angular",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    3,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces::msg::Screw, angular),  // bytes offset in struct
    nullptr,  // default value
    size_function__Screw__angular,  // size() function pointer
    get_const_function__Screw__angular,  // get_const(index) function pointer
    get_function__Screw__angular,  // get(index) function pointer
    fetch_function__Screw__angular,  // fetch(index, &value) function pointer
    assign_function__Screw__angular,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers Screw_message_members = {
  "dls2_interfaces::msg",  // message namespace
  "Screw",  // message name
  2,  // number of fields
  sizeof(dls2_interfaces::msg::Screw),
  Screw_message_member_array,  // message members
  Screw_init_function,  // function to initialize message memory (memory has to be allocated)
  Screw_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t Screw_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &Screw_message_members,
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
get_message_type_support_handle<dls2_interfaces::msg::Screw>()
{
  return &::dls2_interfaces::msg::rosidl_typesupport_introspection_cpp::Screw_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, dls2_interfaces, msg, Screw)() {
  return &::dls2_interfaces::msg::rosidl_typesupport_introspection_cpp::Screw_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
