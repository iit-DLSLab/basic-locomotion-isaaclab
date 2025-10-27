// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from dls2_interfaces:msg/TrajectoryGenerator.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "dls2_interfaces/msg/detail/trajectory_generator__rosidl_typesupport_introspection_c.h"
#include "dls2_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "dls2_interfaces/msg/detail/trajectory_generator__functions.h"
#include "dls2_interfaces/msg/detail/trajectory_generator__struct.h"


// Include directives for member types
// Member `frame_id`
#include "rosidl_runtime_c/string_functions.h"
// Member `com_pose`
#include "dls2_interfaces/msg/pose.h"
// Member `com_pose`
#include "dls2_interfaces/msg/detail/pose__rosidl_typesupport_introspection_c.h"
// Member `com_vel`
// Member `com_acc`
#include "dls2_interfaces/msg/screw.h"
// Member `com_vel`
// Member `com_acc`
#include "dls2_interfaces/msg/detail/screw__rosidl_typesupport_introspection_c.h"
// Member `joints_position`
// Member `joints_velocity`
// Member `joints_acceleration`
// Member `joints_effort`
// Member `kp`
// Member `kd`
// Member `stance_legs`
// Member `nominal_touch_down`
// Member `touch_down`
// Member `swing_period`
// Member `normal_force_max`
// Member `normal_force_min`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__TrajectoryGenerator_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  dls2_interfaces__msg__TrajectoryGenerator__init(message_memory);
}

void dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__TrajectoryGenerator_fini_function(void * message_memory)
{
  dls2_interfaces__msg__TrajectoryGenerator__fini(message_memory);
}

size_t dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__size_function__TrajectoryGenerator__joints_position(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_const_function__TrajectoryGenerator__joints_position(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_function__TrajectoryGenerator__joints_position(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__fetch_function__TrajectoryGenerator__joints_position(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_const_function__TrajectoryGenerator__joints_position(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__assign_function__TrajectoryGenerator__joints_position(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_function__TrajectoryGenerator__joints_position(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__resize_function__TrajectoryGenerator__joints_position(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

size_t dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__size_function__TrajectoryGenerator__joints_velocity(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_const_function__TrajectoryGenerator__joints_velocity(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_function__TrajectoryGenerator__joints_velocity(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__fetch_function__TrajectoryGenerator__joints_velocity(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_const_function__TrajectoryGenerator__joints_velocity(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__assign_function__TrajectoryGenerator__joints_velocity(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_function__TrajectoryGenerator__joints_velocity(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__resize_function__TrajectoryGenerator__joints_velocity(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

size_t dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__size_function__TrajectoryGenerator__joints_acceleration(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_const_function__TrajectoryGenerator__joints_acceleration(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_function__TrajectoryGenerator__joints_acceleration(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__fetch_function__TrajectoryGenerator__joints_acceleration(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_const_function__TrajectoryGenerator__joints_acceleration(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__assign_function__TrajectoryGenerator__joints_acceleration(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_function__TrajectoryGenerator__joints_acceleration(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__resize_function__TrajectoryGenerator__joints_acceleration(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

size_t dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__size_function__TrajectoryGenerator__joints_effort(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_const_function__TrajectoryGenerator__joints_effort(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_function__TrajectoryGenerator__joints_effort(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__fetch_function__TrajectoryGenerator__joints_effort(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_const_function__TrajectoryGenerator__joints_effort(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__assign_function__TrajectoryGenerator__joints_effort(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_function__TrajectoryGenerator__joints_effort(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__resize_function__TrajectoryGenerator__joints_effort(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

size_t dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__size_function__TrajectoryGenerator__kp(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_const_function__TrajectoryGenerator__kp(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_function__TrajectoryGenerator__kp(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__fetch_function__TrajectoryGenerator__kp(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_const_function__TrajectoryGenerator__kp(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__assign_function__TrajectoryGenerator__kp(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_function__TrajectoryGenerator__kp(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__resize_function__TrajectoryGenerator__kp(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

size_t dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__size_function__TrajectoryGenerator__kd(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_const_function__TrajectoryGenerator__kd(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_function__TrajectoryGenerator__kd(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__fetch_function__TrajectoryGenerator__kd(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_const_function__TrajectoryGenerator__kd(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__assign_function__TrajectoryGenerator__kd(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_function__TrajectoryGenerator__kd(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__resize_function__TrajectoryGenerator__kd(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

size_t dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__size_function__TrajectoryGenerator__wrench(
  const void * untyped_member)
{
  (void)untyped_member;
  return 6;
}

const void * dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_const_function__TrajectoryGenerator__wrench(
  const void * untyped_member, size_t index)
{
  const double * member =
    (const double *)(untyped_member);
  return &member[index];
}

void * dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_function__TrajectoryGenerator__wrench(
  void * untyped_member, size_t index)
{
  double * member =
    (double *)(untyped_member);
  return &member[index];
}

void dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__fetch_function__TrajectoryGenerator__wrench(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_const_function__TrajectoryGenerator__wrench(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__assign_function__TrajectoryGenerator__wrench(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_function__TrajectoryGenerator__wrench(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

size_t dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__size_function__TrajectoryGenerator__stance_legs(
  const void * untyped_member)
{
  const rosidl_runtime_c__boolean__Sequence * member =
    (const rosidl_runtime_c__boolean__Sequence *)(untyped_member);
  return member->size;
}

const void * dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_const_function__TrajectoryGenerator__stance_legs(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__boolean__Sequence * member =
    (const rosidl_runtime_c__boolean__Sequence *)(untyped_member);
  return &member->data[index];
}

void * dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_function__TrajectoryGenerator__stance_legs(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__boolean__Sequence * member =
    (rosidl_runtime_c__boolean__Sequence *)(untyped_member);
  return &member->data[index];
}

void dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__fetch_function__TrajectoryGenerator__stance_legs(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const bool * item =
    ((const bool *)
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_const_function__TrajectoryGenerator__stance_legs(untyped_member, index));
  bool * value =
    (bool *)(untyped_value);
  *value = *item;
}

void dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__assign_function__TrajectoryGenerator__stance_legs(
  void * untyped_member, size_t index, const void * untyped_value)
{
  bool * item =
    ((bool *)
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_function__TrajectoryGenerator__stance_legs(untyped_member, index));
  const bool * value =
    (const bool *)(untyped_value);
  *item = *value;
}

bool dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__resize_function__TrajectoryGenerator__stance_legs(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__boolean__Sequence * member =
    (rosidl_runtime_c__boolean__Sequence *)(untyped_member);
  rosidl_runtime_c__boolean__Sequence__fini(member);
  return rosidl_runtime_c__boolean__Sequence__init(member, size);
}

size_t dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__size_function__TrajectoryGenerator__nominal_touch_down(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_const_function__TrajectoryGenerator__nominal_touch_down(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_function__TrajectoryGenerator__nominal_touch_down(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__fetch_function__TrajectoryGenerator__nominal_touch_down(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_const_function__TrajectoryGenerator__nominal_touch_down(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__assign_function__TrajectoryGenerator__nominal_touch_down(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_function__TrajectoryGenerator__nominal_touch_down(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__resize_function__TrajectoryGenerator__nominal_touch_down(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

size_t dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__size_function__TrajectoryGenerator__touch_down(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_const_function__TrajectoryGenerator__touch_down(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_function__TrajectoryGenerator__touch_down(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__fetch_function__TrajectoryGenerator__touch_down(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_const_function__TrajectoryGenerator__touch_down(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__assign_function__TrajectoryGenerator__touch_down(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_function__TrajectoryGenerator__touch_down(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__resize_function__TrajectoryGenerator__touch_down(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

size_t dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__size_function__TrajectoryGenerator__swing_period(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_const_function__TrajectoryGenerator__swing_period(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_function__TrajectoryGenerator__swing_period(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__fetch_function__TrajectoryGenerator__swing_period(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_const_function__TrajectoryGenerator__swing_period(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__assign_function__TrajectoryGenerator__swing_period(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_function__TrajectoryGenerator__swing_period(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__resize_function__TrajectoryGenerator__swing_period(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

size_t dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__size_function__TrajectoryGenerator__normal_force_max(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_const_function__TrajectoryGenerator__normal_force_max(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_function__TrajectoryGenerator__normal_force_max(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__fetch_function__TrajectoryGenerator__normal_force_max(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_const_function__TrajectoryGenerator__normal_force_max(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__assign_function__TrajectoryGenerator__normal_force_max(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_function__TrajectoryGenerator__normal_force_max(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__resize_function__TrajectoryGenerator__normal_force_max(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

size_t dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__size_function__TrajectoryGenerator__normal_force_min(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_const_function__TrajectoryGenerator__normal_force_min(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_function__TrajectoryGenerator__normal_force_min(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__fetch_function__TrajectoryGenerator__normal_force_min(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_const_function__TrajectoryGenerator__normal_force_min(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__assign_function__TrajectoryGenerator__normal_force_min(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_function__TrajectoryGenerator__normal_force_min(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__resize_function__TrajectoryGenerator__normal_force_min(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__TrajectoryGenerator_message_member_array[19] = {
  {
    "frame_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces__msg__TrajectoryGenerator, frame_id),  // bytes offset in struct
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
    offsetof(dls2_interfaces__msg__TrajectoryGenerator, sequence_id),  // bytes offset in struct
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
    offsetof(dls2_interfaces__msg__TrajectoryGenerator, timestamp),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "com_pose",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces__msg__TrajectoryGenerator, com_pose),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "com_vel",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces__msg__TrajectoryGenerator, com_vel),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "com_acc",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces__msg__TrajectoryGenerator, com_acc),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "joints_position",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces__msg__TrajectoryGenerator, joints_position),  // bytes offset in struct
    NULL,  // default value
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__size_function__TrajectoryGenerator__joints_position,  // size() function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_const_function__TrajectoryGenerator__joints_position,  // get_const(index) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_function__TrajectoryGenerator__joints_position,  // get(index) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__fetch_function__TrajectoryGenerator__joints_position,  // fetch(index, &value) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__assign_function__TrajectoryGenerator__joints_position,  // assign(index, value) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__resize_function__TrajectoryGenerator__joints_position  // resize(index) function pointer
  },
  {
    "joints_velocity",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces__msg__TrajectoryGenerator, joints_velocity),  // bytes offset in struct
    NULL,  // default value
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__size_function__TrajectoryGenerator__joints_velocity,  // size() function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_const_function__TrajectoryGenerator__joints_velocity,  // get_const(index) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_function__TrajectoryGenerator__joints_velocity,  // get(index) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__fetch_function__TrajectoryGenerator__joints_velocity,  // fetch(index, &value) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__assign_function__TrajectoryGenerator__joints_velocity,  // assign(index, value) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__resize_function__TrajectoryGenerator__joints_velocity  // resize(index) function pointer
  },
  {
    "joints_acceleration",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces__msg__TrajectoryGenerator, joints_acceleration),  // bytes offset in struct
    NULL,  // default value
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__size_function__TrajectoryGenerator__joints_acceleration,  // size() function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_const_function__TrajectoryGenerator__joints_acceleration,  // get_const(index) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_function__TrajectoryGenerator__joints_acceleration,  // get(index) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__fetch_function__TrajectoryGenerator__joints_acceleration,  // fetch(index, &value) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__assign_function__TrajectoryGenerator__joints_acceleration,  // assign(index, value) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__resize_function__TrajectoryGenerator__joints_acceleration  // resize(index) function pointer
  },
  {
    "joints_effort",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces__msg__TrajectoryGenerator, joints_effort),  // bytes offset in struct
    NULL,  // default value
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__size_function__TrajectoryGenerator__joints_effort,  // size() function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_const_function__TrajectoryGenerator__joints_effort,  // get_const(index) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_function__TrajectoryGenerator__joints_effort,  // get(index) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__fetch_function__TrajectoryGenerator__joints_effort,  // fetch(index, &value) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__assign_function__TrajectoryGenerator__joints_effort,  // assign(index, value) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__resize_function__TrajectoryGenerator__joints_effort  // resize(index) function pointer
  },
  {
    "kp",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces__msg__TrajectoryGenerator, kp),  // bytes offset in struct
    NULL,  // default value
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__size_function__TrajectoryGenerator__kp,  // size() function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_const_function__TrajectoryGenerator__kp,  // get_const(index) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_function__TrajectoryGenerator__kp,  // get(index) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__fetch_function__TrajectoryGenerator__kp,  // fetch(index, &value) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__assign_function__TrajectoryGenerator__kp,  // assign(index, value) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__resize_function__TrajectoryGenerator__kp  // resize(index) function pointer
  },
  {
    "kd",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces__msg__TrajectoryGenerator, kd),  // bytes offset in struct
    NULL,  // default value
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__size_function__TrajectoryGenerator__kd,  // size() function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_const_function__TrajectoryGenerator__kd,  // get_const(index) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_function__TrajectoryGenerator__kd,  // get(index) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__fetch_function__TrajectoryGenerator__kd,  // fetch(index, &value) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__assign_function__TrajectoryGenerator__kd,  // assign(index, value) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__resize_function__TrajectoryGenerator__kd  // resize(index) function pointer
  },
  {
    "wrench",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    6,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces__msg__TrajectoryGenerator, wrench),  // bytes offset in struct
    NULL,  // default value
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__size_function__TrajectoryGenerator__wrench,  // size() function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_const_function__TrajectoryGenerator__wrench,  // get_const(index) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_function__TrajectoryGenerator__wrench,  // get(index) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__fetch_function__TrajectoryGenerator__wrench,  // fetch(index, &value) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__assign_function__TrajectoryGenerator__wrench,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "stance_legs",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces__msg__TrajectoryGenerator, stance_legs),  // bytes offset in struct
    NULL,  // default value
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__size_function__TrajectoryGenerator__stance_legs,  // size() function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_const_function__TrajectoryGenerator__stance_legs,  // get_const(index) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_function__TrajectoryGenerator__stance_legs,  // get(index) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__fetch_function__TrajectoryGenerator__stance_legs,  // fetch(index, &value) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__assign_function__TrajectoryGenerator__stance_legs,  // assign(index, value) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__resize_function__TrajectoryGenerator__stance_legs  // resize(index) function pointer
  },
  {
    "nominal_touch_down",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces__msg__TrajectoryGenerator, nominal_touch_down),  // bytes offset in struct
    NULL,  // default value
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__size_function__TrajectoryGenerator__nominal_touch_down,  // size() function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_const_function__TrajectoryGenerator__nominal_touch_down,  // get_const(index) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_function__TrajectoryGenerator__nominal_touch_down,  // get(index) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__fetch_function__TrajectoryGenerator__nominal_touch_down,  // fetch(index, &value) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__assign_function__TrajectoryGenerator__nominal_touch_down,  // assign(index, value) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__resize_function__TrajectoryGenerator__nominal_touch_down  // resize(index) function pointer
  },
  {
    "touch_down",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces__msg__TrajectoryGenerator, touch_down),  // bytes offset in struct
    NULL,  // default value
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__size_function__TrajectoryGenerator__touch_down,  // size() function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_const_function__TrajectoryGenerator__touch_down,  // get_const(index) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_function__TrajectoryGenerator__touch_down,  // get(index) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__fetch_function__TrajectoryGenerator__touch_down,  // fetch(index, &value) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__assign_function__TrajectoryGenerator__touch_down,  // assign(index, value) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__resize_function__TrajectoryGenerator__touch_down  // resize(index) function pointer
  },
  {
    "swing_period",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces__msg__TrajectoryGenerator, swing_period),  // bytes offset in struct
    NULL,  // default value
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__size_function__TrajectoryGenerator__swing_period,  // size() function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_const_function__TrajectoryGenerator__swing_period,  // get_const(index) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_function__TrajectoryGenerator__swing_period,  // get(index) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__fetch_function__TrajectoryGenerator__swing_period,  // fetch(index, &value) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__assign_function__TrajectoryGenerator__swing_period,  // assign(index, value) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__resize_function__TrajectoryGenerator__swing_period  // resize(index) function pointer
  },
  {
    "normal_force_max",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces__msg__TrajectoryGenerator, normal_force_max),  // bytes offset in struct
    NULL,  // default value
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__size_function__TrajectoryGenerator__normal_force_max,  // size() function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_const_function__TrajectoryGenerator__normal_force_max,  // get_const(index) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_function__TrajectoryGenerator__normal_force_max,  // get(index) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__fetch_function__TrajectoryGenerator__normal_force_max,  // fetch(index, &value) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__assign_function__TrajectoryGenerator__normal_force_max,  // assign(index, value) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__resize_function__TrajectoryGenerator__normal_force_max  // resize(index) function pointer
  },
  {
    "normal_force_min",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces__msg__TrajectoryGenerator, normal_force_min),  // bytes offset in struct
    NULL,  // default value
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__size_function__TrajectoryGenerator__normal_force_min,  // size() function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_const_function__TrajectoryGenerator__normal_force_min,  // get_const(index) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__get_function__TrajectoryGenerator__normal_force_min,  // get(index) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__fetch_function__TrajectoryGenerator__normal_force_min,  // fetch(index, &value) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__assign_function__TrajectoryGenerator__normal_force_min,  // assign(index, value) function pointer
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__resize_function__TrajectoryGenerator__normal_force_min  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__TrajectoryGenerator_message_members = {
  "dls2_interfaces__msg",  // message namespace
  "TrajectoryGenerator",  // message name
  19,  // number of fields
  sizeof(dls2_interfaces__msg__TrajectoryGenerator),
  dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__TrajectoryGenerator_message_member_array,  // message members
  dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__TrajectoryGenerator_init_function,  // function to initialize message memory (memory has to be allocated)
  dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__TrajectoryGenerator_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__TrajectoryGenerator_message_type_support_handle = {
  0,
  &dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__TrajectoryGenerator_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_dls2_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, dls2_interfaces, msg, TrajectoryGenerator)() {
  dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__TrajectoryGenerator_message_member_array[3].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, dls2_interfaces, msg, Pose)();
  dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__TrajectoryGenerator_message_member_array[4].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, dls2_interfaces, msg, Screw)();
  dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__TrajectoryGenerator_message_member_array[5].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, dls2_interfaces, msg, Screw)();
  if (!dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__TrajectoryGenerator_message_type_support_handle.typesupport_identifier) {
    dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__TrajectoryGenerator_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &dls2_interfaces__msg__TrajectoryGenerator__rosidl_typesupport_introspection_c__TrajectoryGenerator_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
