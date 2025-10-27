// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from dls2_interfaces:msg/Screw.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "dls2_interfaces/msg/detail/screw__rosidl_typesupport_introspection_c.h"
#include "dls2_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "dls2_interfaces/msg/detail/screw__functions.h"
#include "dls2_interfaces/msg/detail/screw__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void dls2_interfaces__msg__Screw__rosidl_typesupport_introspection_c__Screw_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  dls2_interfaces__msg__Screw__init(message_memory);
}

void dls2_interfaces__msg__Screw__rosidl_typesupport_introspection_c__Screw_fini_function(void * message_memory)
{
  dls2_interfaces__msg__Screw__fini(message_memory);
}

size_t dls2_interfaces__msg__Screw__rosidl_typesupport_introspection_c__size_function__Screw__linear(
  const void * untyped_member)
{
  (void)untyped_member;
  return 3;
}

const void * dls2_interfaces__msg__Screw__rosidl_typesupport_introspection_c__get_const_function__Screw__linear(
  const void * untyped_member, size_t index)
{
  const double * member =
    (const double *)(untyped_member);
  return &member[index];
}

void * dls2_interfaces__msg__Screw__rosidl_typesupport_introspection_c__get_function__Screw__linear(
  void * untyped_member, size_t index)
{
  double * member =
    (double *)(untyped_member);
  return &member[index];
}

void dls2_interfaces__msg__Screw__rosidl_typesupport_introspection_c__fetch_function__Screw__linear(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    dls2_interfaces__msg__Screw__rosidl_typesupport_introspection_c__get_const_function__Screw__linear(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void dls2_interfaces__msg__Screw__rosidl_typesupport_introspection_c__assign_function__Screw__linear(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    dls2_interfaces__msg__Screw__rosidl_typesupport_introspection_c__get_function__Screw__linear(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

size_t dls2_interfaces__msg__Screw__rosidl_typesupport_introspection_c__size_function__Screw__angular(
  const void * untyped_member)
{
  (void)untyped_member;
  return 3;
}

const void * dls2_interfaces__msg__Screw__rosidl_typesupport_introspection_c__get_const_function__Screw__angular(
  const void * untyped_member, size_t index)
{
  const double * member =
    (const double *)(untyped_member);
  return &member[index];
}

void * dls2_interfaces__msg__Screw__rosidl_typesupport_introspection_c__get_function__Screw__angular(
  void * untyped_member, size_t index)
{
  double * member =
    (double *)(untyped_member);
  return &member[index];
}

void dls2_interfaces__msg__Screw__rosidl_typesupport_introspection_c__fetch_function__Screw__angular(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    dls2_interfaces__msg__Screw__rosidl_typesupport_introspection_c__get_const_function__Screw__angular(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void dls2_interfaces__msg__Screw__rosidl_typesupport_introspection_c__assign_function__Screw__angular(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    dls2_interfaces__msg__Screw__rosidl_typesupport_introspection_c__get_function__Screw__angular(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

static rosidl_typesupport_introspection_c__MessageMember dls2_interfaces__msg__Screw__rosidl_typesupport_introspection_c__Screw_message_member_array[2] = {
  {
    "linear",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    3,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces__msg__Screw, linear),  // bytes offset in struct
    NULL,  // default value
    dls2_interfaces__msg__Screw__rosidl_typesupport_introspection_c__size_function__Screw__linear,  // size() function pointer
    dls2_interfaces__msg__Screw__rosidl_typesupport_introspection_c__get_const_function__Screw__linear,  // get_const(index) function pointer
    dls2_interfaces__msg__Screw__rosidl_typesupport_introspection_c__get_function__Screw__linear,  // get(index) function pointer
    dls2_interfaces__msg__Screw__rosidl_typesupport_introspection_c__fetch_function__Screw__linear,  // fetch(index, &value) function pointer
    dls2_interfaces__msg__Screw__rosidl_typesupport_introspection_c__assign_function__Screw__linear,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "angular",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    3,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces__msg__Screw, angular),  // bytes offset in struct
    NULL,  // default value
    dls2_interfaces__msg__Screw__rosidl_typesupport_introspection_c__size_function__Screw__angular,  // size() function pointer
    dls2_interfaces__msg__Screw__rosidl_typesupport_introspection_c__get_const_function__Screw__angular,  // get_const(index) function pointer
    dls2_interfaces__msg__Screw__rosidl_typesupport_introspection_c__get_function__Screw__angular,  // get(index) function pointer
    dls2_interfaces__msg__Screw__rosidl_typesupport_introspection_c__fetch_function__Screw__angular,  // fetch(index, &value) function pointer
    dls2_interfaces__msg__Screw__rosidl_typesupport_introspection_c__assign_function__Screw__angular,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers dls2_interfaces__msg__Screw__rosidl_typesupport_introspection_c__Screw_message_members = {
  "dls2_interfaces__msg",  // message namespace
  "Screw",  // message name
  2,  // number of fields
  sizeof(dls2_interfaces__msg__Screw),
  dls2_interfaces__msg__Screw__rosidl_typesupport_introspection_c__Screw_message_member_array,  // message members
  dls2_interfaces__msg__Screw__rosidl_typesupport_introspection_c__Screw_init_function,  // function to initialize message memory (memory has to be allocated)
  dls2_interfaces__msg__Screw__rosidl_typesupport_introspection_c__Screw_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t dls2_interfaces__msg__Screw__rosidl_typesupport_introspection_c__Screw_message_type_support_handle = {
  0,
  &dls2_interfaces__msg__Screw__rosidl_typesupport_introspection_c__Screw_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_dls2_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, dls2_interfaces, msg, Screw)() {
  if (!dls2_interfaces__msg__Screw__rosidl_typesupport_introspection_c__Screw_message_type_support_handle.typesupport_identifier) {
    dls2_interfaces__msg__Screw__rosidl_typesupport_introspection_c__Screw_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &dls2_interfaces__msg__Screw__rosidl_typesupport_introspection_c__Screw_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
