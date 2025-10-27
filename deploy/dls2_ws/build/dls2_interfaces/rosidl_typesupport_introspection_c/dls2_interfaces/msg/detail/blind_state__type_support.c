// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from dls2_interfaces:msg/BlindState.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "dls2_interfaces/msg/detail/blind_state__rosidl_typesupport_introspection_c.h"
#include "dls2_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "dls2_interfaces/msg/detail/blind_state__functions.h"
#include "dls2_interfaces/msg/detail/blind_state__struct.h"


// Include directives for member types
// Member `frame_id`
// Member `robot_name`
// Member `joints_name`
#include "rosidl_runtime_c/string_functions.h"
// Member `joints_position`
// Member `joints_velocity`
// Member `joints_acceleration`
// Member `joints_effort`
// Member `joints_temperature`
// Member `feet_contact`
// Member `current_feet_positions`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__BlindState_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  dls2_interfaces__msg__BlindState__init(message_memory);
}

void dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__BlindState_fini_function(void * message_memory)
{
  dls2_interfaces__msg__BlindState__fini(message_memory);
}

size_t dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__size_function__BlindState__joints_name(
  const void * untyped_member)
{
  const rosidl_runtime_c__String__Sequence * member =
    (const rosidl_runtime_c__String__Sequence *)(untyped_member);
  return member->size;
}

const void * dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_const_function__BlindState__joints_name(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__String__Sequence * member =
    (const rosidl_runtime_c__String__Sequence *)(untyped_member);
  return &member->data[index];
}

void * dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_function__BlindState__joints_name(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__String__Sequence * member =
    (rosidl_runtime_c__String__Sequence *)(untyped_member);
  return &member->data[index];
}

void dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__fetch_function__BlindState__joints_name(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const rosidl_runtime_c__String * item =
    ((const rosidl_runtime_c__String *)
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_const_function__BlindState__joints_name(untyped_member, index));
  rosidl_runtime_c__String * value =
    (rosidl_runtime_c__String *)(untyped_value);
  *value = *item;
}

void dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__assign_function__BlindState__joints_name(
  void * untyped_member, size_t index, const void * untyped_value)
{
  rosidl_runtime_c__String * item =
    ((rosidl_runtime_c__String *)
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_function__BlindState__joints_name(untyped_member, index));
  const rosidl_runtime_c__String * value =
    (const rosidl_runtime_c__String *)(untyped_value);
  *item = *value;
}

bool dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__resize_function__BlindState__joints_name(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__String__Sequence * member =
    (rosidl_runtime_c__String__Sequence *)(untyped_member);
  rosidl_runtime_c__String__Sequence__fini(member);
  return rosidl_runtime_c__String__Sequence__init(member, size);
}

size_t dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__size_function__BlindState__joints_position(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_const_function__BlindState__joints_position(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_function__BlindState__joints_position(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__fetch_function__BlindState__joints_position(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_const_function__BlindState__joints_position(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__assign_function__BlindState__joints_position(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_function__BlindState__joints_position(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__resize_function__BlindState__joints_position(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

size_t dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__size_function__BlindState__joints_velocity(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_const_function__BlindState__joints_velocity(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_function__BlindState__joints_velocity(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__fetch_function__BlindState__joints_velocity(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_const_function__BlindState__joints_velocity(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__assign_function__BlindState__joints_velocity(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_function__BlindState__joints_velocity(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__resize_function__BlindState__joints_velocity(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

size_t dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__size_function__BlindState__joints_acceleration(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_const_function__BlindState__joints_acceleration(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_function__BlindState__joints_acceleration(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__fetch_function__BlindState__joints_acceleration(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_const_function__BlindState__joints_acceleration(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__assign_function__BlindState__joints_acceleration(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_function__BlindState__joints_acceleration(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__resize_function__BlindState__joints_acceleration(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

size_t dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__size_function__BlindState__joints_effort(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_const_function__BlindState__joints_effort(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_function__BlindState__joints_effort(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__fetch_function__BlindState__joints_effort(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_const_function__BlindState__joints_effort(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__assign_function__BlindState__joints_effort(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_function__BlindState__joints_effort(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__resize_function__BlindState__joints_effort(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

size_t dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__size_function__BlindState__joints_temperature(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_const_function__BlindState__joints_temperature(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_function__BlindState__joints_temperature(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__fetch_function__BlindState__joints_temperature(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_const_function__BlindState__joints_temperature(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__assign_function__BlindState__joints_temperature(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_function__BlindState__joints_temperature(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__resize_function__BlindState__joints_temperature(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

size_t dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__size_function__BlindState__feet_contact(
  const void * untyped_member)
{
  const rosidl_runtime_c__boolean__Sequence * member =
    (const rosidl_runtime_c__boolean__Sequence *)(untyped_member);
  return member->size;
}

const void * dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_const_function__BlindState__feet_contact(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__boolean__Sequence * member =
    (const rosidl_runtime_c__boolean__Sequence *)(untyped_member);
  return &member->data[index];
}

void * dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_function__BlindState__feet_contact(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__boolean__Sequence * member =
    (rosidl_runtime_c__boolean__Sequence *)(untyped_member);
  return &member->data[index];
}

void dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__fetch_function__BlindState__feet_contact(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const bool * item =
    ((const bool *)
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_const_function__BlindState__feet_contact(untyped_member, index));
  bool * value =
    (bool *)(untyped_value);
  *value = *item;
}

void dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__assign_function__BlindState__feet_contact(
  void * untyped_member, size_t index, const void * untyped_value)
{
  bool * item =
    ((bool *)
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_function__BlindState__feet_contact(untyped_member, index));
  const bool * value =
    (const bool *)(untyped_value);
  *item = *value;
}

bool dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__resize_function__BlindState__feet_contact(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__boolean__Sequence * member =
    (rosidl_runtime_c__boolean__Sequence *)(untyped_member);
  rosidl_runtime_c__boolean__Sequence__fini(member);
  return rosidl_runtime_c__boolean__Sequence__init(member, size);
}

size_t dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__size_function__BlindState__current_feet_positions(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_const_function__BlindState__current_feet_positions(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_function__BlindState__current_feet_positions(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__fetch_function__BlindState__current_feet_positions(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_const_function__BlindState__current_feet_positions(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__assign_function__BlindState__current_feet_positions(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_function__BlindState__current_feet_positions(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__resize_function__BlindState__current_feet_positions(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__BlindState_message_member_array[12] = {
  {
    "frame_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces__msg__BlindState, frame_id),  // bytes offset in struct
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
    offsetof(dls2_interfaces__msg__BlindState, sequence_id),  // bytes offset in struct
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
    offsetof(dls2_interfaces__msg__BlindState, timestamp),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "robot_name",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces__msg__BlindState, robot_name),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "joints_name",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces__msg__BlindState, joints_name),  // bytes offset in struct
    NULL,  // default value
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__size_function__BlindState__joints_name,  // size() function pointer
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_const_function__BlindState__joints_name,  // get_const(index) function pointer
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_function__BlindState__joints_name,  // get(index) function pointer
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__fetch_function__BlindState__joints_name,  // fetch(index, &value) function pointer
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__assign_function__BlindState__joints_name,  // assign(index, value) function pointer
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__resize_function__BlindState__joints_name  // resize(index) function pointer
  },
  {
    "joints_position",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces__msg__BlindState, joints_position),  // bytes offset in struct
    NULL,  // default value
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__size_function__BlindState__joints_position,  // size() function pointer
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_const_function__BlindState__joints_position,  // get_const(index) function pointer
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_function__BlindState__joints_position,  // get(index) function pointer
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__fetch_function__BlindState__joints_position,  // fetch(index, &value) function pointer
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__assign_function__BlindState__joints_position,  // assign(index, value) function pointer
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__resize_function__BlindState__joints_position  // resize(index) function pointer
  },
  {
    "joints_velocity",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces__msg__BlindState, joints_velocity),  // bytes offset in struct
    NULL,  // default value
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__size_function__BlindState__joints_velocity,  // size() function pointer
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_const_function__BlindState__joints_velocity,  // get_const(index) function pointer
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_function__BlindState__joints_velocity,  // get(index) function pointer
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__fetch_function__BlindState__joints_velocity,  // fetch(index, &value) function pointer
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__assign_function__BlindState__joints_velocity,  // assign(index, value) function pointer
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__resize_function__BlindState__joints_velocity  // resize(index) function pointer
  },
  {
    "joints_acceleration",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces__msg__BlindState, joints_acceleration),  // bytes offset in struct
    NULL,  // default value
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__size_function__BlindState__joints_acceleration,  // size() function pointer
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_const_function__BlindState__joints_acceleration,  // get_const(index) function pointer
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_function__BlindState__joints_acceleration,  // get(index) function pointer
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__fetch_function__BlindState__joints_acceleration,  // fetch(index, &value) function pointer
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__assign_function__BlindState__joints_acceleration,  // assign(index, value) function pointer
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__resize_function__BlindState__joints_acceleration  // resize(index) function pointer
  },
  {
    "joints_effort",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces__msg__BlindState, joints_effort),  // bytes offset in struct
    NULL,  // default value
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__size_function__BlindState__joints_effort,  // size() function pointer
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_const_function__BlindState__joints_effort,  // get_const(index) function pointer
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_function__BlindState__joints_effort,  // get(index) function pointer
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__fetch_function__BlindState__joints_effort,  // fetch(index, &value) function pointer
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__assign_function__BlindState__joints_effort,  // assign(index, value) function pointer
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__resize_function__BlindState__joints_effort  // resize(index) function pointer
  },
  {
    "joints_temperature",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces__msg__BlindState, joints_temperature),  // bytes offset in struct
    NULL,  // default value
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__size_function__BlindState__joints_temperature,  // size() function pointer
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_const_function__BlindState__joints_temperature,  // get_const(index) function pointer
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_function__BlindState__joints_temperature,  // get(index) function pointer
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__fetch_function__BlindState__joints_temperature,  // fetch(index, &value) function pointer
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__assign_function__BlindState__joints_temperature,  // assign(index, value) function pointer
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__resize_function__BlindState__joints_temperature  // resize(index) function pointer
  },
  {
    "feet_contact",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces__msg__BlindState, feet_contact),  // bytes offset in struct
    NULL,  // default value
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__size_function__BlindState__feet_contact,  // size() function pointer
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_const_function__BlindState__feet_contact,  // get_const(index) function pointer
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_function__BlindState__feet_contact,  // get(index) function pointer
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__fetch_function__BlindState__feet_contact,  // fetch(index, &value) function pointer
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__assign_function__BlindState__feet_contact,  // assign(index, value) function pointer
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__resize_function__BlindState__feet_contact  // resize(index) function pointer
  },
  {
    "current_feet_positions",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces__msg__BlindState, current_feet_positions),  // bytes offset in struct
    NULL,  // default value
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__size_function__BlindState__current_feet_positions,  // size() function pointer
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_const_function__BlindState__current_feet_positions,  // get_const(index) function pointer
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__get_function__BlindState__current_feet_positions,  // get(index) function pointer
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__fetch_function__BlindState__current_feet_positions,  // fetch(index, &value) function pointer
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__assign_function__BlindState__current_feet_positions,  // assign(index, value) function pointer
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__resize_function__BlindState__current_feet_positions  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__BlindState_message_members = {
  "dls2_interfaces__msg",  // message namespace
  "BlindState",  // message name
  12,  // number of fields
  sizeof(dls2_interfaces__msg__BlindState),
  dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__BlindState_message_member_array,  // message members
  dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__BlindState_init_function,  // function to initialize message memory (memory has to be allocated)
  dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__BlindState_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__BlindState_message_type_support_handle = {
  0,
  &dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__BlindState_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_dls2_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, dls2_interfaces, msg, BlindState)() {
  if (!dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__BlindState_message_type_support_handle.typesupport_identifier) {
    dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__BlindState_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &dls2_interfaces__msg__BlindState__rosidl_typesupport_introspection_c__BlindState_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
