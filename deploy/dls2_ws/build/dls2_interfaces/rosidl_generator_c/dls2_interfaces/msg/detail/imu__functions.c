// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from dls2_interfaces:msg/Imu.idl
// generated code does not contain a copyright notice
#include "dls2_interfaces/msg/detail/imu__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `frame_id`
#include "rosidl_runtime_c/string_functions.h"

bool
dls2_interfaces__msg__Imu__init(dls2_interfaces__msg__Imu * msg)
{
  if (!msg) {
    return false;
  }
  // frame_id
  if (!rosidl_runtime_c__String__init(&msg->frame_id)) {
    dls2_interfaces__msg__Imu__fini(msg);
    return false;
  }
  // sequence_id
  // timestamp
  // orientation
  // orientation_rpy
  // orientation_covariance
  // angular_velocity
  // angular_velocity_covariance
  // linear_acceleration
  // linear_acceleration_covariance
  return true;
}

void
dls2_interfaces__msg__Imu__fini(dls2_interfaces__msg__Imu * msg)
{
  if (!msg) {
    return;
  }
  // frame_id
  rosidl_runtime_c__String__fini(&msg->frame_id);
  // sequence_id
  // timestamp
  // orientation
  // orientation_rpy
  // orientation_covariance
  // angular_velocity
  // angular_velocity_covariance
  // linear_acceleration
  // linear_acceleration_covariance
}

bool
dls2_interfaces__msg__Imu__are_equal(const dls2_interfaces__msg__Imu * lhs, const dls2_interfaces__msg__Imu * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // frame_id
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->frame_id), &(rhs->frame_id)))
  {
    return false;
  }
  // sequence_id
  if (lhs->sequence_id != rhs->sequence_id) {
    return false;
  }
  // timestamp
  if (lhs->timestamp != rhs->timestamp) {
    return false;
  }
  // orientation
  for (size_t i = 0; i < 4; ++i) {
    if (lhs->orientation[i] != rhs->orientation[i]) {
      return false;
    }
  }
  // orientation_rpy
  for (size_t i = 0; i < 3; ++i) {
    if (lhs->orientation_rpy[i] != rhs->orientation_rpy[i]) {
      return false;
    }
  }
  // orientation_covariance
  for (size_t i = 0; i < 9; ++i) {
    if (lhs->orientation_covariance[i] != rhs->orientation_covariance[i]) {
      return false;
    }
  }
  // angular_velocity
  for (size_t i = 0; i < 3; ++i) {
    if (lhs->angular_velocity[i] != rhs->angular_velocity[i]) {
      return false;
    }
  }
  // angular_velocity_covariance
  for (size_t i = 0; i < 9; ++i) {
    if (lhs->angular_velocity_covariance[i] != rhs->angular_velocity_covariance[i]) {
      return false;
    }
  }
  // linear_acceleration
  for (size_t i = 0; i < 3; ++i) {
    if (lhs->linear_acceleration[i] != rhs->linear_acceleration[i]) {
      return false;
    }
  }
  // linear_acceleration_covariance
  for (size_t i = 0; i < 9; ++i) {
    if (lhs->linear_acceleration_covariance[i] != rhs->linear_acceleration_covariance[i]) {
      return false;
    }
  }
  return true;
}

bool
dls2_interfaces__msg__Imu__copy(
  const dls2_interfaces__msg__Imu * input,
  dls2_interfaces__msg__Imu * output)
{
  if (!input || !output) {
    return false;
  }
  // frame_id
  if (!rosidl_runtime_c__String__copy(
      &(input->frame_id), &(output->frame_id)))
  {
    return false;
  }
  // sequence_id
  output->sequence_id = input->sequence_id;
  // timestamp
  output->timestamp = input->timestamp;
  // orientation
  for (size_t i = 0; i < 4; ++i) {
    output->orientation[i] = input->orientation[i];
  }
  // orientation_rpy
  for (size_t i = 0; i < 3; ++i) {
    output->orientation_rpy[i] = input->orientation_rpy[i];
  }
  // orientation_covariance
  for (size_t i = 0; i < 9; ++i) {
    output->orientation_covariance[i] = input->orientation_covariance[i];
  }
  // angular_velocity
  for (size_t i = 0; i < 3; ++i) {
    output->angular_velocity[i] = input->angular_velocity[i];
  }
  // angular_velocity_covariance
  for (size_t i = 0; i < 9; ++i) {
    output->angular_velocity_covariance[i] = input->angular_velocity_covariance[i];
  }
  // linear_acceleration
  for (size_t i = 0; i < 3; ++i) {
    output->linear_acceleration[i] = input->linear_acceleration[i];
  }
  // linear_acceleration_covariance
  for (size_t i = 0; i < 9; ++i) {
    output->linear_acceleration_covariance[i] = input->linear_acceleration_covariance[i];
  }
  return true;
}

dls2_interfaces__msg__Imu *
dls2_interfaces__msg__Imu__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  dls2_interfaces__msg__Imu * msg = (dls2_interfaces__msg__Imu *)allocator.allocate(sizeof(dls2_interfaces__msg__Imu), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(dls2_interfaces__msg__Imu));
  bool success = dls2_interfaces__msg__Imu__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
dls2_interfaces__msg__Imu__destroy(dls2_interfaces__msg__Imu * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    dls2_interfaces__msg__Imu__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
dls2_interfaces__msg__Imu__Sequence__init(dls2_interfaces__msg__Imu__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  dls2_interfaces__msg__Imu * data = NULL;

  if (size) {
    data = (dls2_interfaces__msg__Imu *)allocator.zero_allocate(size, sizeof(dls2_interfaces__msg__Imu), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = dls2_interfaces__msg__Imu__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        dls2_interfaces__msg__Imu__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
dls2_interfaces__msg__Imu__Sequence__fini(dls2_interfaces__msg__Imu__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      dls2_interfaces__msg__Imu__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

dls2_interfaces__msg__Imu__Sequence *
dls2_interfaces__msg__Imu__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  dls2_interfaces__msg__Imu__Sequence * array = (dls2_interfaces__msg__Imu__Sequence *)allocator.allocate(sizeof(dls2_interfaces__msg__Imu__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = dls2_interfaces__msg__Imu__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
dls2_interfaces__msg__Imu__Sequence__destroy(dls2_interfaces__msg__Imu__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    dls2_interfaces__msg__Imu__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
dls2_interfaces__msg__Imu__Sequence__are_equal(const dls2_interfaces__msg__Imu__Sequence * lhs, const dls2_interfaces__msg__Imu__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!dls2_interfaces__msg__Imu__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
dls2_interfaces__msg__Imu__Sequence__copy(
  const dls2_interfaces__msg__Imu__Sequence * input,
  dls2_interfaces__msg__Imu__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(dls2_interfaces__msg__Imu);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    dls2_interfaces__msg__Imu * data =
      (dls2_interfaces__msg__Imu *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!dls2_interfaces__msg__Imu__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          dls2_interfaces__msg__Imu__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!dls2_interfaces__msg__Imu__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
