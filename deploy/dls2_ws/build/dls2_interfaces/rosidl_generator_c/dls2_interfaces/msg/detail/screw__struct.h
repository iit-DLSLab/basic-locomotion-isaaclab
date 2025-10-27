// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from dls2_interfaces:msg/Screw.idl
// generated code does not contain a copyright notice

#ifndef DLS2_INTERFACES__MSG__DETAIL__SCREW__STRUCT_H_
#define DLS2_INTERFACES__MSG__DETAIL__SCREW__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/Screw in the package dls2_interfaces.
typedef struct dls2_interfaces__msg__Screw
{
  double linear[3];
  double angular[3];
} dls2_interfaces__msg__Screw;

// Struct for a sequence of dls2_interfaces__msg__Screw.
typedef struct dls2_interfaces__msg__Screw__Sequence
{
  dls2_interfaces__msg__Screw * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} dls2_interfaces__msg__Screw__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // DLS2_INTERFACES__MSG__DETAIL__SCREW__STRUCT_H_
