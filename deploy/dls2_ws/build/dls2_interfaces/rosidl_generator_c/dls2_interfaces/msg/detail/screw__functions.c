// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from dls2_interfaces:msg/Screw.idl
// generated code does not contain a copyright notice
#include "dls2_interfaces/msg/detail/screw__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
dls2_interfaces__msg__Screw__init(dls2_interfaces__msg__Screw * msg)
{
  if (!msg) {
    return false;
  }
  // linear
  // angular
  return true;
}

void
dls2_interfaces__msg__Screw__fini(dls2_interfaces__msg__Screw * msg)
{
  if (!msg) {
    return;
  }
  // linear
  // angular
}

bool
dls2_interfaces__msg__Screw__are_equal(const dls2_interfaces__msg__Screw * lhs, const dls2_interfaces__msg__Screw * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // linear
  for (size_t i = 0; i < 3; ++i) {
    if (lhs->linear[i] != rhs->linear[i]) {
      return false;
    }
  }
  // angular
  for (size_t i = 0; i < 3; ++i) {
    if (lhs->angular[i] != rhs->angular[i]) {
      return false;
    }
  }
  return true;
}

bool
dls2_interfaces__msg__Screw__copy(
  const dls2_interfaces__msg__Screw * input,
  dls2_interfaces__msg__Screw * output)
{
  if (!input || !output) {
    return false;
  }
  // linear
  for (size_t i = 0; i < 3; ++i) {
    output->linear[i] = input->linear[i];
  }
  // angular
  for (size_t i = 0; i < 3; ++i) {
    output->angular[i] = input->angular[i];
  }
  return true;
}

dls2_interfaces__msg__Screw *
dls2_interfaces__msg__Screw__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  dls2_interfaces__msg__Screw * msg = (dls2_interfaces__msg__Screw *)allocator.allocate(sizeof(dls2_interfaces__msg__Screw), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(dls2_interfaces__msg__Screw));
  bool success = dls2_interfaces__msg__Screw__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
dls2_interfaces__msg__Screw__destroy(dls2_interfaces__msg__Screw * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    dls2_interfaces__msg__Screw__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
dls2_interfaces__msg__Screw__Sequence__init(dls2_interfaces__msg__Screw__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  dls2_interfaces__msg__Screw * data = NULL;

  if (size) {
    data = (dls2_interfaces__msg__Screw *)allocator.zero_allocate(size, sizeof(dls2_interfaces__msg__Screw), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = dls2_interfaces__msg__Screw__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        dls2_interfaces__msg__Screw__fini(&data[i - 1]);
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
dls2_interfaces__msg__Screw__Sequence__fini(dls2_interfaces__msg__Screw__Sequence * array)
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
      dls2_interfaces__msg__Screw__fini(&array->data[i]);
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

dls2_interfaces__msg__Screw__Sequence *
dls2_interfaces__msg__Screw__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  dls2_interfaces__msg__Screw__Sequence * array = (dls2_interfaces__msg__Screw__Sequence *)allocator.allocate(sizeof(dls2_interfaces__msg__Screw__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = dls2_interfaces__msg__Screw__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
dls2_interfaces__msg__Screw__Sequence__destroy(dls2_interfaces__msg__Screw__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    dls2_interfaces__msg__Screw__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
dls2_interfaces__msg__Screw__Sequence__are_equal(const dls2_interfaces__msg__Screw__Sequence * lhs, const dls2_interfaces__msg__Screw__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!dls2_interfaces__msg__Screw__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
dls2_interfaces__msg__Screw__Sequence__copy(
  const dls2_interfaces__msg__Screw__Sequence * input,
  dls2_interfaces__msg__Screw__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(dls2_interfaces__msg__Screw);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    dls2_interfaces__msg__Screw * data =
      (dls2_interfaces__msg__Screw *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!dls2_interfaces__msg__Screw__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          dls2_interfaces__msg__Screw__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!dls2_interfaces__msg__Screw__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
