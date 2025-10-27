// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from dls2_interfaces:msg/Imu.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "dls2_interfaces/msg/detail/imu__rosidl_typesupport_introspection_c.h"
#include "dls2_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "dls2_interfaces/msg/detail/imu__functions.h"
#include "dls2_interfaces/msg/detail/imu__struct.h"


// Include directives for member types
// Member `frame_id`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__Imu_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  dls2_interfaces__msg__Imu__init(message_memory);
}

void dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__Imu_fini_function(void * message_memory)
{
  dls2_interfaces__msg__Imu__fini(message_memory);
}

size_t dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__size_function__Imu__orientation(
  const void * untyped_member)
{
  (void)untyped_member;
  return 4;
}

const void * dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__get_const_function__Imu__orientation(
  const void * untyped_member, size_t index)
{
  const double * member =
    (const double *)(untyped_member);
  return &member[index];
}

void * dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__get_function__Imu__orientation(
  void * untyped_member, size_t index)
{
  double * member =
    (double *)(untyped_member);
  return &member[index];
}

void dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__fetch_function__Imu__orientation(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__get_const_function__Imu__orientation(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__assign_function__Imu__orientation(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__get_function__Imu__orientation(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

size_t dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__size_function__Imu__orientation_rpy(
  const void * untyped_member)
{
  (void)untyped_member;
  return 3;
}

const void * dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__get_const_function__Imu__orientation_rpy(
  const void * untyped_member, size_t index)
{
  const double * member =
    (const double *)(untyped_member);
  return &member[index];
}

void * dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__get_function__Imu__orientation_rpy(
  void * untyped_member, size_t index)
{
  double * member =
    (double *)(untyped_member);
  return &member[index];
}

void dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__fetch_function__Imu__orientation_rpy(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__get_const_function__Imu__orientation_rpy(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__assign_function__Imu__orientation_rpy(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__get_function__Imu__orientation_rpy(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

size_t dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__size_function__Imu__orientation_covariance(
  const void * untyped_member)
{
  (void)untyped_member;
  return 9;
}

const void * dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__get_const_function__Imu__orientation_covariance(
  const void * untyped_member, size_t index)
{
  const double * member =
    (const double *)(untyped_member);
  return &member[index];
}

void * dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__get_function__Imu__orientation_covariance(
  void * untyped_member, size_t index)
{
  double * member =
    (double *)(untyped_member);
  return &member[index];
}

void dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__fetch_function__Imu__orientation_covariance(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__get_const_function__Imu__orientation_covariance(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__assign_function__Imu__orientation_covariance(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__get_function__Imu__orientation_covariance(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

size_t dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__size_function__Imu__angular_velocity(
  const void * untyped_member)
{
  (void)untyped_member;
  return 3;
}

const void * dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__get_const_function__Imu__angular_velocity(
  const void * untyped_member, size_t index)
{
  const double * member =
    (const double *)(untyped_member);
  return &member[index];
}

void * dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__get_function__Imu__angular_velocity(
  void * untyped_member, size_t index)
{
  double * member =
    (double *)(untyped_member);
  return &member[index];
}

void dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__fetch_function__Imu__angular_velocity(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__get_const_function__Imu__angular_velocity(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__assign_function__Imu__angular_velocity(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__get_function__Imu__angular_velocity(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

size_t dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__size_function__Imu__angular_velocity_covariance(
  const void * untyped_member)
{
  (void)untyped_member;
  return 9;
}

const void * dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__get_const_function__Imu__angular_velocity_covariance(
  const void * untyped_member, size_t index)
{
  const double * member =
    (const double *)(untyped_member);
  return &member[index];
}

void * dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__get_function__Imu__angular_velocity_covariance(
  void * untyped_member, size_t index)
{
  double * member =
    (double *)(untyped_member);
  return &member[index];
}

void dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__fetch_function__Imu__angular_velocity_covariance(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__get_const_function__Imu__angular_velocity_covariance(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__assign_function__Imu__angular_velocity_covariance(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__get_function__Imu__angular_velocity_covariance(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

size_t dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__size_function__Imu__linear_acceleration(
  const void * untyped_member)
{
  (void)untyped_member;
  return 3;
}

const void * dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__get_const_function__Imu__linear_acceleration(
  const void * untyped_member, size_t index)
{
  const double * member =
    (const double *)(untyped_member);
  return &member[index];
}

void * dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__get_function__Imu__linear_acceleration(
  void * untyped_member, size_t index)
{
  double * member =
    (double *)(untyped_member);
  return &member[index];
}

void dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__fetch_function__Imu__linear_acceleration(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__get_const_function__Imu__linear_acceleration(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__assign_function__Imu__linear_acceleration(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__get_function__Imu__linear_acceleration(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

size_t dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__size_function__Imu__linear_acceleration_covariance(
  const void * untyped_member)
{
  (void)untyped_member;
  return 9;
}

const void * dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__get_const_function__Imu__linear_acceleration_covariance(
  const void * untyped_member, size_t index)
{
  const double * member =
    (const double *)(untyped_member);
  return &member[index];
}

void * dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__get_function__Imu__linear_acceleration_covariance(
  void * untyped_member, size_t index)
{
  double * member =
    (double *)(untyped_member);
  return &member[index];
}

void dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__fetch_function__Imu__linear_acceleration_covariance(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__get_const_function__Imu__linear_acceleration_covariance(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__assign_function__Imu__linear_acceleration_covariance(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__get_function__Imu__linear_acceleration_covariance(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

static rosidl_typesupport_introspection_c__MessageMember dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__Imu_message_member_array[10] = {
  {
    "frame_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces__msg__Imu, frame_id),  // bytes offset in struct
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
    offsetof(dls2_interfaces__msg__Imu, sequence_id),  // bytes offset in struct
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
    offsetof(dls2_interfaces__msg__Imu, timestamp),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "orientation",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    4,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces__msg__Imu, orientation),  // bytes offset in struct
    NULL,  // default value
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__size_function__Imu__orientation,  // size() function pointer
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__get_const_function__Imu__orientation,  // get_const(index) function pointer
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__get_function__Imu__orientation,  // get(index) function pointer
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__fetch_function__Imu__orientation,  // fetch(index, &value) function pointer
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__assign_function__Imu__orientation,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "orientation_rpy",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    3,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces__msg__Imu, orientation_rpy),  // bytes offset in struct
    NULL,  // default value
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__size_function__Imu__orientation_rpy,  // size() function pointer
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__get_const_function__Imu__orientation_rpy,  // get_const(index) function pointer
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__get_function__Imu__orientation_rpy,  // get(index) function pointer
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__fetch_function__Imu__orientation_rpy,  // fetch(index, &value) function pointer
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__assign_function__Imu__orientation_rpy,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "orientation_covariance",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    9,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces__msg__Imu, orientation_covariance),  // bytes offset in struct
    NULL,  // default value
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__size_function__Imu__orientation_covariance,  // size() function pointer
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__get_const_function__Imu__orientation_covariance,  // get_const(index) function pointer
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__get_function__Imu__orientation_covariance,  // get(index) function pointer
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__fetch_function__Imu__orientation_covariance,  // fetch(index, &value) function pointer
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__assign_function__Imu__orientation_covariance,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "angular_velocity",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    3,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces__msg__Imu, angular_velocity),  // bytes offset in struct
    NULL,  // default value
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__size_function__Imu__angular_velocity,  // size() function pointer
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__get_const_function__Imu__angular_velocity,  // get_const(index) function pointer
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__get_function__Imu__angular_velocity,  // get(index) function pointer
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__fetch_function__Imu__angular_velocity,  // fetch(index, &value) function pointer
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__assign_function__Imu__angular_velocity,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "angular_velocity_covariance",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    9,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces__msg__Imu, angular_velocity_covariance),  // bytes offset in struct
    NULL,  // default value
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__size_function__Imu__angular_velocity_covariance,  // size() function pointer
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__get_const_function__Imu__angular_velocity_covariance,  // get_const(index) function pointer
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__get_function__Imu__angular_velocity_covariance,  // get(index) function pointer
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__fetch_function__Imu__angular_velocity_covariance,  // fetch(index, &value) function pointer
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__assign_function__Imu__angular_velocity_covariance,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "linear_acceleration",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    3,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces__msg__Imu, linear_acceleration),  // bytes offset in struct
    NULL,  // default value
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__size_function__Imu__linear_acceleration,  // size() function pointer
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__get_const_function__Imu__linear_acceleration,  // get_const(index) function pointer
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__get_function__Imu__linear_acceleration,  // get(index) function pointer
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__fetch_function__Imu__linear_acceleration,  // fetch(index, &value) function pointer
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__assign_function__Imu__linear_acceleration,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "linear_acceleration_covariance",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    9,  // array size
    false,  // is upper bound
    offsetof(dls2_interfaces__msg__Imu, linear_acceleration_covariance),  // bytes offset in struct
    NULL,  // default value
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__size_function__Imu__linear_acceleration_covariance,  // size() function pointer
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__get_const_function__Imu__linear_acceleration_covariance,  // get_const(index) function pointer
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__get_function__Imu__linear_acceleration_covariance,  // get(index) function pointer
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__fetch_function__Imu__linear_acceleration_covariance,  // fetch(index, &value) function pointer
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__assign_function__Imu__linear_acceleration_covariance,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__Imu_message_members = {
  "dls2_interfaces__msg",  // message namespace
  "Imu",  // message name
  10,  // number of fields
  sizeof(dls2_interfaces__msg__Imu),
  dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__Imu_message_member_array,  // message members
  dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__Imu_init_function,  // function to initialize message memory (memory has to be allocated)
  dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__Imu_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__Imu_message_type_support_handle = {
  0,
  &dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__Imu_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_dls2_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, dls2_interfaces, msg, Imu)() {
  if (!dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__Imu_message_type_support_handle.typesupport_identifier) {
    dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__Imu_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &dls2_interfaces__msg__Imu__rosidl_typesupport_introspection_c__Imu_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
