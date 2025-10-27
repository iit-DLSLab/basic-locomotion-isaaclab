// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from dls2_interfaces:msg/TrajectoryGenerator.idl
// generated code does not contain a copyright notice

#ifndef DLS2_INTERFACES__MSG__DETAIL__TRAJECTORY_GENERATOR__STRUCT_H_
#define DLS2_INTERFACES__MSG__DETAIL__TRAJECTORY_GENERATOR__STRUCT_H_

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
#include "rosidl_runtime_c/string.h"
// Member 'com_pose'
#include "dls2_interfaces/msg/detail/pose__struct.h"
// Member 'com_vel'
// Member 'com_acc'
#include "dls2_interfaces/msg/detail/screw__struct.h"
// Member 'joints_position'
// Member 'joints_velocity'
// Member 'joints_acceleration'
// Member 'joints_effort'
// Member 'kp'
// Member 'kd'
// Member 'stance_legs'
// Member 'nominal_touch_down'
// Member 'touch_down'
// Member 'swing_period'
// Member 'normal_force_max'
// Member 'normal_force_min'
#include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in msg/TrajectoryGenerator in the package dls2_interfaces.
typedef struct dls2_interfaces__msg__TrajectoryGenerator
{
  rosidl_runtime_c__String frame_id;
  uint32_t sequence_id;
  double timestamp;
  dls2_interfaces__msg__Pose com_pose;
  dls2_interfaces__msg__Screw com_vel;
  dls2_interfaces__msg__Screw com_acc;
  rosidl_runtime_c__double__Sequence joints_position;
  rosidl_runtime_c__double__Sequence joints_velocity;
  rosidl_runtime_c__double__Sequence joints_acceleration;
  rosidl_runtime_c__double__Sequence joints_effort;
  rosidl_runtime_c__double__Sequence kp;
  rosidl_runtime_c__double__Sequence kd;
  double wrench[6];
  rosidl_runtime_c__boolean__Sequence stance_legs;
  rosidl_runtime_c__double__Sequence nominal_touch_down;
  rosidl_runtime_c__double__Sequence touch_down;
  rosidl_runtime_c__double__Sequence swing_period;
  rosidl_runtime_c__double__Sequence normal_force_max;
  rosidl_runtime_c__double__Sequence normal_force_min;
} dls2_interfaces__msg__TrajectoryGenerator;

// Struct for a sequence of dls2_interfaces__msg__TrajectoryGenerator.
typedef struct dls2_interfaces__msg__TrajectoryGenerator__Sequence
{
  dls2_interfaces__msg__TrajectoryGenerator * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} dls2_interfaces__msg__TrajectoryGenerator__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // DLS2_INTERFACES__MSG__DETAIL__TRAJECTORY_GENERATOR__STRUCT_H_
