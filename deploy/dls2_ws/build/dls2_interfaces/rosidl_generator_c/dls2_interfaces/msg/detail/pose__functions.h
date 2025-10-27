// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from dls2_interfaces:msg/Pose.idl
// generated code does not contain a copyright notice

#ifndef DLS2_INTERFACES__MSG__DETAIL__POSE__FUNCTIONS_H_
#define DLS2_INTERFACES__MSG__DETAIL__POSE__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "dls2_interfaces/msg/rosidl_generator_c__visibility_control.h"

#include "dls2_interfaces/msg/detail/pose__struct.h"

/// Initialize msg/Pose message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * dls2_interfaces__msg__Pose
 * )) before or use
 * dls2_interfaces__msg__Pose__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_dls2_interfaces
bool
dls2_interfaces__msg__Pose__init(dls2_interfaces__msg__Pose * msg);

/// Finalize msg/Pose message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_dls2_interfaces
void
dls2_interfaces__msg__Pose__fini(dls2_interfaces__msg__Pose * msg);

/// Create msg/Pose message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * dls2_interfaces__msg__Pose__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_dls2_interfaces
dls2_interfaces__msg__Pose *
dls2_interfaces__msg__Pose__create();

/// Destroy msg/Pose message.
/**
 * It calls
 * dls2_interfaces__msg__Pose__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_dls2_interfaces
void
dls2_interfaces__msg__Pose__destroy(dls2_interfaces__msg__Pose * msg);

/// Check for msg/Pose message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_dls2_interfaces
bool
dls2_interfaces__msg__Pose__are_equal(const dls2_interfaces__msg__Pose * lhs, const dls2_interfaces__msg__Pose * rhs);

/// Copy a msg/Pose message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_dls2_interfaces
bool
dls2_interfaces__msg__Pose__copy(
  const dls2_interfaces__msg__Pose * input,
  dls2_interfaces__msg__Pose * output);

/// Initialize array of msg/Pose messages.
/**
 * It allocates the memory for the number of elements and calls
 * dls2_interfaces__msg__Pose__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_dls2_interfaces
bool
dls2_interfaces__msg__Pose__Sequence__init(dls2_interfaces__msg__Pose__Sequence * array, size_t size);

/// Finalize array of msg/Pose messages.
/**
 * It calls
 * dls2_interfaces__msg__Pose__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_dls2_interfaces
void
dls2_interfaces__msg__Pose__Sequence__fini(dls2_interfaces__msg__Pose__Sequence * array);

/// Create array of msg/Pose messages.
/**
 * It allocates the memory for the array and calls
 * dls2_interfaces__msg__Pose__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_dls2_interfaces
dls2_interfaces__msg__Pose__Sequence *
dls2_interfaces__msg__Pose__Sequence__create(size_t size);

/// Destroy array of msg/Pose messages.
/**
 * It calls
 * dls2_interfaces__msg__Pose__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_dls2_interfaces
void
dls2_interfaces__msg__Pose__Sequence__destroy(dls2_interfaces__msg__Pose__Sequence * array);

/// Check for msg/Pose message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_dls2_interfaces
bool
dls2_interfaces__msg__Pose__Sequence__are_equal(const dls2_interfaces__msg__Pose__Sequence * lhs, const dls2_interfaces__msg__Pose__Sequence * rhs);

/// Copy an array of msg/Pose messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_dls2_interfaces
bool
dls2_interfaces__msg__Pose__Sequence__copy(
  const dls2_interfaces__msg__Pose__Sequence * input,
  dls2_interfaces__msg__Pose__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // DLS2_INTERFACES__MSG__DETAIL__POSE__FUNCTIONS_H_
