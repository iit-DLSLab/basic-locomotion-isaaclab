// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from dls2_interfaces:msg/BlindState.idl
// generated code does not contain a copyright notice
#include "dls2_interfaces/msg/detail/blind_state__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `frame_id`
// Member `robot_name`
// Member `joints_name`
#include "rosidl_runtime_c/string_functions.h"
// Member `joints_position`
// Member `joints_velocity`
// Member `joints_acceleration`
// Member `joints_effort`
// Member `joints_temperature`
// Member `feet_contact`
// Member `current_feet_positions`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

bool
dls2_interfaces__msg__BlindState__init(dls2_interfaces__msg__BlindState * msg)
{
  if (!msg) {
    return false;
  }
  // frame_id
  if (!rosidl_runtime_c__String__init(&msg->frame_id)) {
    dls2_interfaces__msg__BlindState__fini(msg);
    return false;
  }
  // sequence_id
  // timestamp
  // robot_name
  if (!rosidl_runtime_c__String__init(&msg->robot_name)) {
    dls2_interfaces__msg__BlindState__fini(msg);
    return false;
  }
  // joints_name
  if (!rosidl_runtime_c__String__Sequence__init(&msg->joints_name, 0)) {
    dls2_interfaces__msg__BlindState__fini(msg);
    return false;
  }
  // joints_position
  if (!rosidl_runtime_c__double__Sequence__init(&msg->joints_position, 0)) {
    dls2_interfaces__msg__BlindState__fini(msg);
    return false;
  }
  // joints_velocity
  if (!rosidl_runtime_c__double__Sequence__init(&msg->joints_velocity, 0)) {
    dls2_interfaces__msg__BlindState__fini(msg);
    return false;
  }
  // joints_acceleration
  if (!rosidl_runtime_c__double__Sequence__init(&msg->joints_acceleration, 0)) {
    dls2_interfaces__msg__BlindState__fini(msg);
    return false;
  }
  // joints_effort
  if (!rosidl_runtime_c__double__Sequence__init(&msg->joints_effort, 0)) {
    dls2_interfaces__msg__BlindState__fini(msg);
    return false;
  }
  // joints_temperature
  if (!rosidl_runtime_c__double__Sequence__init(&msg->joints_temperature, 0)) {
    dls2_interfaces__msg__BlindState__fini(msg);
    return false;
  }
  // feet_contact
  if (!rosidl_runtime_c__boolean__Sequence__init(&msg->feet_contact, 0)) {
    dls2_interfaces__msg__BlindState__fini(msg);
    return false;
  }
  // current_feet_positions
  if (!rosidl_runtime_c__double__Sequence__init(&msg->current_feet_positions, 0)) {
    dls2_interfaces__msg__BlindState__fini(msg);
    return false;
  }
  return true;
}

void
dls2_interfaces__msg__BlindState__fini(dls2_interfaces__msg__BlindState * msg)
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
  // joints_name
  rosidl_runtime_c__String__Sequence__fini(&msg->joints_name);
  // joints_position
  rosidl_runtime_c__double__Sequence__fini(&msg->joints_position);
  // joints_velocity
  rosidl_runtime_c__double__Sequence__fini(&msg->joints_velocity);
  // joints_acceleration
  rosidl_runtime_c__double__Sequence__fini(&msg->joints_acceleration);
  // joints_effort
  rosidl_runtime_c__double__Sequence__fini(&msg->joints_effort);
  // joints_temperature
  rosidl_runtime_c__double__Sequence__fini(&msg->joints_temperature);
  // feet_contact
  rosidl_runtime_c__boolean__Sequence__fini(&msg->feet_contact);
  // current_feet_positions
  rosidl_runtime_c__double__Sequence__fini(&msg->current_feet_positions);
}

bool
dls2_interfaces__msg__BlindState__are_equal(const dls2_interfaces__msg__BlindState * lhs, const dls2_interfaces__msg__BlindState * rhs)
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
  // joints_name
  if (!rosidl_runtime_c__String__Sequence__are_equal(
      &(lhs->joints_name), &(rhs->joints_name)))
  {
    return false;
  }
  // joints_position
  if (!rosidl_runtime_c__double__Sequence__are_equal(
      &(lhs->joints_position), &(rhs->joints_position)))
  {
    return false;
  }
  // joints_velocity
  if (!rosidl_runtime_c__double__Sequence__are_equal(
      &(lhs->joints_velocity), &(rhs->joints_velocity)))
  {
    return false;
  }
  // joints_acceleration
  if (!rosidl_runtime_c__double__Sequence__are_equal(
      &(lhs->joints_acceleration), &(rhs->joints_acceleration)))
  {
    return false;
  }
  // joints_effort
  if (!rosidl_runtime_c__double__Sequence__are_equal(
      &(lhs->joints_effort), &(rhs->joints_effort)))
  {
    return false;
  }
  // joints_temperature
  if (!rosidl_runtime_c__double__Sequence__are_equal(
      &(lhs->joints_temperature), &(rhs->joints_temperature)))
  {
    return false;
  }
  // feet_contact
  if (!rosidl_runtime_c__boolean__Sequence__are_equal(
      &(lhs->feet_contact), &(rhs->feet_contact)))
  {
    return false;
  }
  // current_feet_positions
  if (!rosidl_runtime_c__double__Sequence__are_equal(
      &(lhs->current_feet_positions), &(rhs->current_feet_positions)))
  {
    return false;
  }
  return true;
}

bool
dls2_interfaces__msg__BlindState__copy(
  const dls2_interfaces__msg__BlindState * input,
  dls2_interfaces__msg__BlindState * output)
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
  // joints_name
  if (!rosidl_runtime_c__String__Sequence__copy(
      &(input->joints_name), &(output->joints_name)))
  {
    return false;
  }
  // joints_position
  if (!rosidl_runtime_c__double__Sequence__copy(
      &(input->joints_position), &(output->joints_position)))
  {
    return false;
  }
  // joints_velocity
  if (!rosidl_runtime_c__double__Sequence__copy(
      &(input->joints_velocity), &(output->joints_velocity)))
  {
    return false;
  }
  // joints_acceleration
  if (!rosidl_runtime_c__double__Sequence__copy(
      &(input->joints_acceleration), &(output->joints_acceleration)))
  {
    return false;
  }
  // joints_effort
  if (!rosidl_runtime_c__double__Sequence__copy(
      &(input->joints_effort), &(output->joints_effort)))
  {
    return false;
  }
  // joints_temperature
  if (!rosidl_runtime_c__double__Sequence__copy(
      &(input->joints_temperature), &(output->joints_temperature)))
  {
    return false;
  }
  // feet_contact
  if (!rosidl_runtime_c__boolean__Sequence__copy(
      &(input->feet_contact), &(output->feet_contact)))
  {
    return false;
  }
  // current_feet_positions
  if (!rosidl_runtime_c__double__Sequence__copy(
      &(input->current_feet_positions), &(output->current_feet_positions)))
  {
    return false;
  }
  return true;
}

dls2_interfaces__msg__BlindState *
dls2_interfaces__msg__BlindState__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  dls2_interfaces__msg__BlindState * msg = (dls2_interfaces__msg__BlindState *)allocator.allocate(sizeof(dls2_interfaces__msg__BlindState), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(dls2_interfaces__msg__BlindState));
  bool success = dls2_interfaces__msg__BlindState__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
dls2_interfaces__msg__BlindState__destroy(dls2_interfaces__msg__BlindState * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    dls2_interfaces__msg__BlindState__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
dls2_interfaces__msg__BlindState__Sequence__init(dls2_interfaces__msg__BlindState__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  dls2_interfaces__msg__BlindState * data = NULL;

  if (size) {
    data = (dls2_interfaces__msg__BlindState *)allocator.zero_allocate(size, sizeof(dls2_interfaces__msg__BlindState), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = dls2_interfaces__msg__BlindState__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        dls2_interfaces__msg__BlindState__fini(&data[i - 1]);
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
dls2_interfaces__msg__BlindState__Sequence__fini(dls2_interfaces__msg__BlindState__Sequence * array)
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
      dls2_interfaces__msg__BlindState__fini(&array->data[i]);
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

dls2_interfaces__msg__BlindState__Sequence *
dls2_interfaces__msg__BlindState__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  dls2_interfaces__msg__BlindState__Sequence * array = (dls2_interfaces__msg__BlindState__Sequence *)allocator.allocate(sizeof(dls2_interfaces__msg__BlindState__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = dls2_interfaces__msg__BlindState__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
dls2_interfaces__msg__BlindState__Sequence__destroy(dls2_interfaces__msg__BlindState__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    dls2_interfaces__msg__BlindState__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
dls2_interfaces__msg__BlindState__Sequence__are_equal(const dls2_interfaces__msg__BlindState__Sequence * lhs, const dls2_interfaces__msg__BlindState__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!dls2_interfaces__msg__BlindState__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
dls2_interfaces__msg__BlindState__Sequence__copy(
  const dls2_interfaces__msg__BlindState__Sequence * input,
  dls2_interfaces__msg__BlindState__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(dls2_interfaces__msg__BlindState);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    dls2_interfaces__msg__BlindState * data =
      (dls2_interfaces__msg__BlindState *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!dls2_interfaces__msg__BlindState__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          dls2_interfaces__msg__BlindState__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!dls2_interfaces__msg__BlindState__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
