// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from dls2_interfaces:msg/DesiredTorques.idl
// generated code does not contain a copyright notice

#ifndef DLS2_INTERFACES__MSG__DETAIL__DESIRED_TORQUES__FUNCTIONS_H_
#define DLS2_INTERFACES__MSG__DETAIL__DESIRED_TORQUES__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "dls2_interfaces/msg/rosidl_generator_c__visibility_control.h"

#include "dls2_interfaces/msg/detail/desired_torques__struct.h"

/// Initialize msg/DesiredTorques message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * dls2_interfaces__msg__DesiredTorques
 * )) before or use
 * dls2_interfaces__msg__DesiredTorques__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_dls2_interfaces
bool
dls2_interfaces__msg__DesiredTorques__init(dls2_interfaces__msg__DesiredTorques * msg);

/// Finalize msg/DesiredTorques message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_dls2_interfaces
void
dls2_interfaces__msg__DesiredTorques__fini(dls2_interfaces__msg__DesiredTorques * msg);

/// Create msg/DesiredTorques message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * dls2_interfaces__msg__DesiredTorques__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_dls2_interfaces
dls2_interfaces__msg__DesiredTorques *
dls2_interfaces__msg__DesiredTorques__create();

/// Destroy msg/DesiredTorques message.
/**
 * It calls
 * dls2_interfaces__msg__DesiredTorques__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_dls2_interfaces
void
dls2_interfaces__msg__DesiredTorques__destroy(dls2_interfaces__msg__DesiredTorques * msg);

/// Check for msg/DesiredTorques message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_dls2_interfaces
bool
dls2_interfaces__msg__DesiredTorques__are_equal(const dls2_interfaces__msg__DesiredTorques * lhs, const dls2_interfaces__msg__DesiredTorques * rhs);

/// Copy a msg/DesiredTorques message.
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
dls2_interfaces__msg__DesiredTorques__copy(
  const dls2_interfaces__msg__DesiredTorques * input,
  dls2_interfaces__msg__DesiredTorques * output);

/// Initialize array of msg/DesiredTorques messages.
/**
 * It allocates the memory for the number of elements and calls
 * dls2_interfaces__msg__DesiredTorques__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_dls2_interfaces
bool
dls2_interfaces__msg__DesiredTorques__Sequence__init(dls2_interfaces__msg__DesiredTorques__Sequence * array, size_t size);

/// Finalize array of msg/DesiredTorques messages.
/**
 * It calls
 * dls2_interfaces__msg__DesiredTorques__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_dls2_interfaces
void
dls2_interfaces__msg__DesiredTorques__Sequence__fini(dls2_interfaces__msg__DesiredTorques__Sequence * array);

/// Create array of msg/DesiredTorques messages.
/**
 * It allocates the memory for the array and calls
 * dls2_interfaces__msg__DesiredTorques__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_dls2_interfaces
dls2_interfaces__msg__DesiredTorques__Sequence *
dls2_interfaces__msg__DesiredTorques__Sequence__create(size_t size);

/// Destroy array of msg/DesiredTorques messages.
/**
 * It calls
 * dls2_interfaces__msg__DesiredTorques__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_dls2_interfaces
void
dls2_interfaces__msg__DesiredTorques__Sequence__destroy(dls2_interfaces__msg__DesiredTorques__Sequence * array);

/// Check for msg/DesiredTorques message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_dls2_interfaces
bool
dls2_interfaces__msg__DesiredTorques__Sequence__are_equal(const dls2_interfaces__msg__DesiredTorques__Sequence * lhs, const dls2_interfaces__msg__DesiredTorques__Sequence * rhs);

/// Copy an array of msg/DesiredTorques messages.
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
dls2_interfaces__msg__DesiredTorques__Sequence__copy(
  const dls2_interfaces__msg__DesiredTorques__Sequence * input,
  dls2_interfaces__msg__DesiredTorques__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // DLS2_INTERFACES__MSG__DETAIL__DESIRED_TORQUES__FUNCTIONS_H_
