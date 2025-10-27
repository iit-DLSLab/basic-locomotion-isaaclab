// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from dls2_interfaces:msg/BaseState.idl
// generated code does not contain a copyright notice
#include "dls2_interfaces/msg/detail/base_state__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `frame_id`
// Member `robot_name`
#include "rosidl_runtime_c/string_functions.h"
// Member `pose`
#include "dls2_interfaces/msg/detail/pose__functions.h"
// Member `velocity`
// Member `acceleration`
#include "dls2_interfaces/msg/detail/screw__functions.h"
// Member `stance_status`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

bool
dls2_interfaces__msg__BaseState__init(dls2_interfaces__msg__BaseState * msg)
{
  if (!msg) {
    return false;
  }
  // frame_id
  if (!rosidl_runtime_c__String__init(&msg->frame_id)) {
    dls2_interfaces__msg__BaseState__fini(msg);
    return false;
  }
  // sequence_id
  // timestamp
  // robot_name
  if (!rosidl_runtime_c__String__init(&msg->robot_name)) {
    dls2_interfaces__msg__BaseState__fini(msg);
    return false;
  }
  // pose
  if (!dls2_interfaces__msg__Pose__init(&msg->pose)) {
    dls2_interfaces__msg__BaseState__fini(msg);
    return false;
  }
  // velocity
  if (!dls2_interfaces__msg__Screw__init(&msg->velocity)) {
    dls2_interfaces__msg__BaseState__fini(msg);
    return false;
  }
  // acceleration
  if (!dls2_interfaces__msg__Screw__init(&msg->acceleration)) {
    dls2_interfaces__msg__BaseState__fini(msg);
    return false;
  }
  // stance_status
  if (!rosidl_runtime_c__boolean__Sequence__init(&msg->stance_status, 0)) {
    dls2_interfaces__msg__BaseState__fini(msg);
    return false;
  }
  return true;
}

void
dls2_interfaces__msg__BaseState__fini(dls2_interfaces__msg__BaseState * msg)
{
  if (!msg) {
    return;
  }
  // frame_id
  rosidl_runtime_c__String__fini(&msg->frame_id);
  // sequence_id
  // timestamp
  // robot_name
  rosidl_runtime_c__String__fini(&msg->robot_name);
  // pose
  dls2_interfaces__msg__Pose__fini(&msg->pose);
  // velocity
  dls2_interfaces__msg__Screw__fini(&msg->velocity);
  // acceleration
  dls2_interfaces__msg__Screw__fini(&msg->acceleration);
  // stance_status
  rosidl_runtime_c__boolean__Sequence__fini(&msg->stance_status);
}

bool
dls2_interfaces__msg__BaseState__are_equal(const dls2_interfaces__msg__BaseState * lhs, const dls2_interfaces__msg__BaseState * rhs)
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
  // robot_name
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->robot_name), &(rhs->robot_name)))
  {
    return false;
  }
  // pose
  if (!dls2_interfaces__msg__Pose__are_equal(
      &(lhs->pose), &(rhs->pose)))
  {
    return false;
  }
  // velocity
  if (!dls2_interfaces__msg__Screw__are_equal(
      &(lhs->velocity), &(rhs->velocity)))
  {
    return false;
  }
  // acceleration
  if (!dls2_interfaces__msg__Screw__are_equal(
      &(lhs->acceleration), &(rhs->acceleration)))
  {
    return false;
  }
  // stance_status
  if (!rosidl_runtime_c__boolean__Sequence__are_equal(
      &(lhs->stance_status), &(rhs->stance_status)))
  {
    return false;
  }
  return true;
}

bool
dls2_interfaces__msg__BaseState__copy(
  const dls2_interfaces__msg__BaseState * input,
  dls2_interfaces__msg__BaseState * output)
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
  // robot_name
  if (!rosidl_runtime_c__String__copy(
      &(input->robot_name), &(output->robot_name)))
  {
    return false;
  }
  // pose
  if (!dls2_interfaces__msg__Pose__copy(
      &(input->pose), &(output->pose)))
  {
    return false;
  }
  // velocity
  if (!dls2_interfaces__msg__Screw__copy(
      &(input->velocity), &(output->velocity)))
  {
    return false;
  }
  // acceleration
  if (!dls2_interfaces__msg__Screw__copy(
      &(input->acceleration), &(output->acceleration)))
  {
    return false;
  }
  // stance_status
  if (!rosidl_runtime_c__boolean__Sequence__copy(
      &(input->stance_status), &(output->stance_status)))
  {
    return false;
  }
  return true;
}

dls2_interfaces__msg__BaseState *
dls2_interfaces__msg__BaseState__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  dls2_interfaces__msg__BaseState * msg = (dls2_interfaces__msg__BaseState *)allocator.allocate(sizeof(dls2_interfaces__msg__BaseState), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(dls2_interfaces__msg__BaseState));
  bool success = dls2_interfaces__msg__BaseState__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
dls2_interfaces__msg__BaseState__destroy(dls2_interfaces__msg__BaseState * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    dls2_interfaces__msg__BaseState__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
dls2_interfaces__msg__BaseState__Sequence__init(dls2_interfaces__msg__BaseState__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  dls2_interfaces__msg__BaseState * data = NULL;

  if (size) {
    data = (dls2_interfaces__msg__BaseState *)allocator.zero_allocate(size, sizeof(dls2_interfaces__msg__BaseState), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = dls2_interfaces__msg__BaseState__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        dls2_interfaces__msg__BaseState__fini(&data[i - 1]);
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
dls2_interfaces__msg__BaseState__Sequence__fini(dls2_interfaces__msg__BaseState__Sequence * array)
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
      dls2_interfaces__msg__BaseState__fini(&array->data[i]);
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

dls2_interfaces__msg__BaseState__Sequence *
dls2_interfaces__msg__BaseState__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  dls2_interfaces__msg__BaseState__Sequence * array = (dls2_interfaces__msg__BaseState__Sequence *)allocator.allocate(sizeof(dls2_interfaces__msg__BaseState__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = dls2_interfaces__msg__BaseState__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
dls2_interfaces__msg__BaseState__Sequence__destroy(dls2_interfaces__msg__BaseState__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    dls2_interfaces__msg__BaseState__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
dls2_interfaces__msg__BaseState__Sequence__are_equal(const dls2_interfaces__msg__BaseState__Sequence * lhs, const dls2_interfaces__msg__BaseState__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!dls2_interfaces__msg__BaseState__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
dls2_interfaces__msg__BaseState__Sequence__copy(
  const dls2_interfaces__msg__BaseState__Sequence * input,
  dls2_interfaces__msg__BaseState__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(dls2_interfaces__msg__BaseState);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    dls2_interfaces__msg__BaseState * data =
      (dls2_interfaces__msg__BaseState *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!dls2_interfaces__msg__BaseState__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          dls2_interfaces__msg__BaseState__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!dls2_interfaces__msg__BaseState__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
