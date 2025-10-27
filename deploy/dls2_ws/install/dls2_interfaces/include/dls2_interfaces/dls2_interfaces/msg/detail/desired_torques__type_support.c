// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from dls2_interfaces:msg/DesiredTorques.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "dls2_interfaces/msg/detail/desired_torques__rosidl_typesupport_introspection_c.h"
#include "dls2_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "dls2_interfaces/msg/detail/desired_torques__functions.h"
#include "dls2_interfaces/msg/detail/desired_torques__struct.h"


// Include directives for member types
// Member `frame_id`
#include "rosidl_runtime_c/string_functions.h"
// Member `desired_torques`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void dls2_interfaces__msg__DesiredTorques__rosidl_typesupport_introspection_c__DesiredTorques_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  dls2_interfaces__msg__DesiredTorques__init(message_memory);
}

void dls2_interfaces__msg__DesiredTorques__rosidl_typesupport_introspection_c__DesiredTorques_fini_function(void * message_memory)
{
  dls2_interfaces__msg__DesiredTorques__fini(message_memory);
}

size_t dls2_interfaces__msg__DesiredTorques__rosidl_typesupport_introspection_c__size_function__DesiredTorques__desired_torques(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * dls2_interfaces__msg__DesiredTorques__rosidl_typesupport_introspection_c__get_const_function__DesiredTorques__desired_torques(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * dls2_interfaces__msg__DesiredTorques__rosidl_typesupport_introspection_c__get_function__DesiredTorques__desired_torques(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void dls2_interfaces__msg__DesiredTorques__rosidl_typesupport_introspection_c__fetch_function__DesiredTorques__desired_torques(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    dls2_interfaces__msg__DesiredTorques__rosidl_typesupport_introspection_c__get_const_function__DesiredTorques__desired_torques(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void dls2_interfaces__msg__DesiredTorques__rosidl_typesupport_introspection_c__assign_function__DesiredTorques__desired_torques(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    dls2_interfaces__msg__DesiredTorques__rosidl_typesupport_introspection_c__get_function__DesiredTorques__desired_torques(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool dls2_interfaces__msg__DesiredTorques__rosidl_typesupport_introspection_c__resize_function__DesiredTorques__desired_torques(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember dls2_interfaces__msg__DesiredTorques__rosidl_typesupport_introspection_c__DesiredTorques_message_member_array[4] = {
  {
    "frame_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces__msg__DesiredTorques, frame_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "sequence_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces__msg__DesiredTorques, sequence_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "timestamp",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces__msg__DesiredTorques, timestamp),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "desired_torques",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces__msg__DesiredTorques, desired_torques),  // bytes offset in struct
    NULL,  // default value
    dls2_interfaces__msg__DesiredTorques__rosidl_typesupport_introspection_c__size_function__DesiredTorques__desired_torques,  // size() function pointer
    dls2_interfaces__msg__DesiredTorques__rosidl_typesupport_introspection_c__get_const_function__DesiredTorques__desired_torques,  // get_const(index) function pointer
    dls2_interfaces__msg__DesiredTorques__rosidl_typesupport_introspection_c__get_function__DesiredTorques__desired_torques,  // get(index) function pointer
    dls2_interfaces__msg__DesiredTorques__rosidl_typesupport_introspection_c__fetch_function__DesiredTorques__desired_torques,  // fetch(index, &value) function pointer
    dls2_interfaces__msg__DesiredTorques__rosidl_typesupport_introspection_c__assign_function__DesiredTorques__desired_torques,  // assign(index, value) function pointer
    dls2_interfaces__msg__DesiredTorques__rosidl_typesupport_introspection_c__resize_function__DesiredTorques__desired_torques  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers dls2_interfaces__msg__DesiredTorques__rosidl_typesupport_introspection_c__DesiredTorques_message_members = {
  "dls2_interfaces__msg",  // message namespace
  "DesiredTorques",  // message name
  4,  // number of fields
  sizeof(dls2_interfaces__msg__DesiredTorques),
  dls2_interfaces__msg__DesiredTorques__rosidl_typesupport_introspection_c__DesiredTorques_message_member_array,  // message members
  dls2_interfaces__msg__DesiredTorques__rosidl_typesupport_introspection_c__DesiredTorques_init_function,  // function to initialize message memory (memory has to be allocated)
  dls2_interfaces__msg__DesiredTorques__rosidl_typesupport_introspection_c__DesiredTorques_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t dls2_interfaces__msg__DesiredTorques__rosidl_typesupport_introspection_c__DesiredTorques_message_type_support_handle = {
  0,
  &dls2_interfaces__msg__DesiredTorques__rosidl_typesupport_introspection_c__DesiredTorques_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_dls2_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, dls2_interfaces, msg, DesiredTorques)() {
  if (!dls2_interfaces__msg__DesiredTorques__rosidl_typesupport_introspection_c__DesiredTorques_message_type_support_handle.typesupport_identifier) {
    dls2_interfaces__msg__DesiredTorques__rosidl_typesupport_introspection_c__DesiredTorques_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &dls2_interfaces__msg__DesiredTorques__rosidl_typesupport_introspection_c__DesiredTorques_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
