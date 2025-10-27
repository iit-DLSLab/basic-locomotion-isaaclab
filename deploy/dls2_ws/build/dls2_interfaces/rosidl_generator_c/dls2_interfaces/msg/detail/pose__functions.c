// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from dls2_interfaces:msg/Pose.idl
// generated code does not contain a copyright notice
#include "dls2_interfaces/msg/detail/pose__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
dls2_interfaces__msg__Pose__init(dls2_interfaces__msg__Pose * msg)
{
  if (!msg) {
    return false;
  }
  // position
  // orientation
  return true;
}

void
dls2_interfaces__msg__Pose__fini(dls2_interfaces__msg__Pose * msg)
{
  if (!msg) {
    return;
  }
  // position
  // orientation
}

bool
dls2_interfaces__msg__Pose__are_equal(const dls2_interfaces__msg__Pose * lhs, const dls2_interfaces__msg__Pose * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // position
  for (size_t i = 0; i < 3; ++i) {
    if (lhs->position[i] != rhs->position[i]) {
      return false;
    }
  }
  // orientation
  for (size_t i = 0; i < 4; ++i) {
    if (lhs->orientation[i] != rhs->orientation[i]) {
      return false;
    }
  }
  return true;
}

bool
dls2_interfaces__msg__Pose__copy(
  const dls2_interfaces__msg__Pose * input,
  dls2_interfaces__msg__Pose * output)
{
  if (!input || !output) {
    return false;
  }
  // position
  for (size_t i = 0; i < 3; ++i) {
    output->position[i] = input->position[i];
  }
  // orientation
  for (size_t i = 0; i < 4; ++i) {
    output->orientation[i] = input->orientation[i];
  }
  return true;
}

dls2_interfaces__msg__Pose *
dls2_interfaces__msg__Pose__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  dls2_interfaces__msg__Pose * msg = (dls2_interfaces__msg__Pose *)allocator.allocate(sizeof(dls2_interfaces__msg__Pose), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(dls2_interfaces__msg__Pose));
  bool success = dls2_interfaces__msg__Pose__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
dls2_interfaces__msg__Pose__destroy(dls2_interfaces__msg__Pose * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    dls2_interfaces__msg__Pose__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
dls2_interfaces__msg__Pose__Sequence__init(dls2_interfaces__msg__Pose__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  dls2_interfaces__msg__Pose * data = NULL;

  if (size) {
    data = (dls2_interfaces__msg__Pose *)allocator.zero_allocate(size, sizeof(dls2_interfaces__msg__Pose), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = dls2_interfaces__msg__Pose__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        dls2_interfaces__msg__Pose__fini(&data[i - 1]);
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
dls2_interfaces__msg__Pose__Sequence__fini(dls2_interfaces__msg__Pose__Sequence * array)
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
      dls2_interfaces__msg__Pose__fini(&array->data[i]);
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

dls2_interfaces__msg__Pose__Sequence *
dls2_interfaces__msg__Pose__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  dls2_interfaces__msg__Pose__Sequence * array = (dls2_interfaces__msg__Pose__Sequence *)allocator.allocate(sizeof(dls2_interfaces__msg__Pose__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = dls2_interfaces__msg__Pose__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
dls2_interfaces__msg__Pose__Sequence__destroy(dls2_interfaces__msg__Pose__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    dls2_interfaces__msg__Pose__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
dls2_interfaces__msg__Pose__Sequence__are_equal(const dls2_interfaces__msg__Pose__Sequence * lhs, const dls2_interfaces__msg__Pose__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!dls2_interfaces__msg__Pose__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
dls2_interfaces__msg__Pose__Sequence__copy(
  const dls2_interfaces__msg__Pose__Sequence * input,
  dls2_interfaces__msg__Pose__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(dls2_interfaces__msg__Pose);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    dls2_interfaces__msg__Pose * data =
      (dls2_interfaces__msg__Pose *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!dls2_interfaces__msg__Pose__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          dls2_interfaces__msg__Pose__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!dls2_interfaces__msg__Pose__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
