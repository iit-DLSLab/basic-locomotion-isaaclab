// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from dls2_interfaces:msg/BlindState.idl
// generated code does not contain a copyright notice

#ifndef DLS2_INTERFACES__MSG__DETAIL__BLIND_STATE__STRUCT_H_
#define DLS2_INTERFACES__MSG__DETAIL__BLIND_STATE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'frame_id'
// Member 'robot_name'
// Member 'joints_name'
#include "rosidl_runtime_c/string.h"
// Member 'joints_position'
// Member 'joints_velocity'
// Member 'joints_acceleration'
// Member 'joints_effort'
// Member 'joints_temperature'
// Member 'feet_contact'
// Member 'current_feet_positions'
#include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in msg/BlindState in the package dls2_interfaces.
typedef struct dls2_interfaces__msg__BlindState
{
  rosidl_runtime_c__String frame_id;
  uint32_t sequence_id;
  double timestamp;
  rosidl_runtime_c__String robot_name;
  rosidl_runtime_c__String__Sequence joints_name;
  rosidl_runtime_c__double__Sequence joints_position;
  rosidl_runtime_c__double__Sequence joints_velocity;
  rosidl_runtime_c__double__Sequence joints_acceleration;
  rosidl_runtime_c__double__Sequence joints_effort;
  rosidl_runtime_c__double__Sequence joints_temperature;
  rosidl_runtime_c__boolean__Sequence feet_contact;
  rosidl_runtime_c__double__Sequence current_feet_positions;
} dls2_interfaces__msg__BlindState;

// Struct for a sequence of dls2_interfaces__msg__BlindState.
typedef struct dls2_interfaces__msg__BlindState__Sequence
{
  dls2_interfaces__msg__BlindState * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} dls2_interfaces__msg__BlindState__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // DLS2_INTERFACES__MSG__DETAIL__BLIND_STATE__STRUCT_H_
