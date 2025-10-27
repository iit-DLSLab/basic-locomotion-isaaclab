// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from dls2_interfaces:msg/TrajectoryGenerator.idl
// generated code does not contain a copyright notice
#include "dls2_interfaces/msg/detail/trajectory_generator__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `frame_id`
#include "rosidl_runtime_c/string_functions.h"
// Member `com_pose`
#include "dls2_interfaces/msg/detail/pose__functions.h"
// Member `com_vel`
// Member `com_acc`
#include "dls2_interfaces/msg/detail/screw__functions.h"
// Member `joints_position`
// Member `joints_velocity`
// Member `joints_acceleration`
// Member `joints_effort`
// Member `kp`
// Member `kd`
// Member `stance_legs`
// Member `nominal_touch_down`
// Member `touch_down`
// Member `swing_period`
// Member `normal_force_max`
// Member `normal_force_min`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

bool
dls2_interfaces__msg__TrajectoryGenerator__init(dls2_interfaces__msg__TrajectoryGenerator * msg)
{
  if (!msg) {
    return false;
  }
  // frame_id
  if (!rosidl_runtime_c__String__init(&msg->frame_id)) {
    dls2_interfaces__msg__TrajectoryGenerator__fini(msg);
    return false;
  }
  // sequence_id
  // timestamp
  // com_pose
  if (!dls2_interfaces__msg__Pose__init(&msg->com_pose)) {
    dls2_interfaces__msg__TrajectoryGenerator__fini(msg);
    return false;
  }
  // com_vel
  if (!dls2_interfaces__msg__Screw__init(&msg->com_vel)) {
    dls2_interfaces__msg__TrajectoryGenerator__fini(msg);
    return false;
  }
  // com_acc
  if (!dls2_interfaces__msg__Screw__init(&msg->com_acc)) {
    dls2_interfaces__msg__TrajectoryGenerator__fini(msg);
    return false;
  }
  // joints_position
  if (!rosidl_runtime_c__double__Sequence__init(&msg->joints_position, 0)) {
    dls2_interfaces__msg__TrajectoryGenerator__fini(msg);
    return false;
  }
  // joints_velocity
  if (!rosidl_runtime_c__double__Sequence__init(&msg->joints_velocity, 0)) {
    dls2_interfaces__msg__TrajectoryGenerator__fini(msg);
    return false;
  }
  // joints_acceleration
  if (!rosidl_runtime_c__double__Sequence__init(&msg->joints_acceleration, 0)) {
    dls2_interfaces__msg__TrajectoryGenerator__fini(msg);
    return false;
  }
  // joints_effort
  if (!rosidl_runtime_c__double__Sequence__init(&msg->joints_effort, 0)) {
    dls2_interfaces__msg__TrajectoryGenerator__fini(msg);
    return false;
  }
  // kp
  if (!rosidl_runtime_c__double__Sequence__init(&msg->kp, 0)) {
    dls2_interfaces__msg__TrajectoryGenerator__fini(msg);
    return false;
  }
  // kd
  if (!rosidl_runtime_c__double__Sequence__init(&msg->kd, 0)) {
    dls2_interfaces__msg__TrajectoryGenerator__fini(msg);
    return false;
  }
  // wrench
  // stance_legs
  if (!rosidl_runtime_c__boolean__Sequence__init(&msg->stance_legs, 0)) {
    dls2_interfaces__msg__TrajectoryGenerator__fini(msg);
    return false;
  }
  // nominal_touch_down
  if (!rosidl_runtime_c__double__Sequence__init(&msg->nominal_touch_down, 0)) {
    dls2_interfaces__msg__TrajectoryGenerator__fini(msg);
    return false;
  }
  // touch_down
  if (!rosidl_runtime_c__double__Sequence__init(&msg->touch_down, 0)) {
    dls2_interfaces__msg__TrajectoryGenerator__fini(msg);
    return false;
  }
  // swing_period
  if (!rosidl_runtime_c__double__Sequence__init(&msg->swing_period, 0)) {
    dls2_interfaces__msg__TrajectoryGenerator__fini(msg);
    return false;
  }
  // normal_force_max
  if (!rosidl_runtime_c__double__Sequence__init(&msg->normal_force_max, 0)) {
    dls2_interfaces__msg__TrajectoryGenerator__fini(msg);
    return false;
  }
  // normal_force_min
  if (!rosidl_runtime_c__double__Sequence__init(&msg->normal_force_min, 0)) {
    dls2_interfaces__msg__TrajectoryGenerator__fini(msg);
    return false;
  }
  return true;
}

void
dls2_interfaces__msg__TrajectoryGenerator__fini(dls2_interfaces__msg__TrajectoryGenerator * msg)
{
  if (!msg) {
    return;
  }
  // frame_id
  rosidl_runtime_c__String__fini(&msg->frame_id);
  // sequence_id
  // timestamp
  // com_pose
  dls2_interfaces__msg__Pose__fini(&msg->com_pose);
  // com_vel
  dls2_interfaces__msg__Screw__fini(&msg->com_vel);
  // com_acc
  dls2_interfaces__msg__Screw__fini(&msg->com_acc);
  // joints_position
  rosidl_runtime_c__double__Sequence__fini(&msg->joints_position);
  // joints_velocity
  rosidl_runtime_c__double__Sequence__fini(&msg->joints_velocity);
  // joints_acceleration
  rosidl_runtime_c__double__Sequence__fini(&msg->joints_acceleration);
  // joints_effort
  rosidl_runtime_c__double__Sequence__fini(&msg->joints_effort);
  // kp
  rosidl_runtime_c__double__Sequence__fini(&msg->kp);
  // kd
  rosidl_runtime_c__double__Sequence__fini(&msg->kd);
  // wrench
  // stance_legs
  rosidl_runtime_c__boolean__Sequence__fini(&msg->stance_legs);
  // nominal_touch_down
  rosidl_runtime_c__double__Sequence__fini(&msg->nominal_touch_down);
  // touch_down
  rosidl_runtime_c__double__Sequence__fini(&msg->touch_down);
  // swing_period
  rosidl_runtime_c__double__Sequence__fini(&msg->swing_period);
  // normal_force_max
  rosidl_runtime_c__double__Sequence__fini(&msg->normal_force_max);
  // normal_force_min
  rosidl_runtime_c__double__Sequence__fini(&msg->normal_force_min);
}

bool
dls2_interfaces__msg__TrajectoryGenerator__are_equal(const dls2_interfaces__msg__TrajectoryGenerator * lhs, const dls2_interfaces__msg__TrajectoryGenerator * rhs)
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
  // com_pose
  if (!dls2_interfaces__msg__Pose__are_equal(
      &(lhs->com_pose), &(rhs->com_pose)))
  {
    return false;
  }
  // com_vel
  if (!dls2_interfaces__msg__Screw__are_equal(
      &(lhs->com_vel), &(rhs->com_vel)))
  {
    return false;
  }
  // com_acc
  if (!dls2_interfaces__msg__Screw__are_equal(
      &(lhs->com_acc), &(rhs->com_acc)))
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
  // kp
  if (!rosidl_runtime_c__double__Sequence__are_equal(
      &(lhs->kp), &(rhs->kp)))
  {
    return false;
  }
  // kd
  if (!rosidl_runtime_c__double__Sequence__are_equal(
      &(lhs->kd), &(rhs->kd)))
  {
    return false;
  }
  // wrench
  for (size_t i = 0; i < 6; ++i) {
    if (lhs->wrench[i] != rhs->wrench[i]) {
      return false;
    }
  }
  // stance_legs
  if (!rosidl_runtime_c__boolean__Sequence__are_equal(
      &(lhs->stance_legs), &(rhs->stance_legs)))
  {
    return false;
  }
  // nominal_touch_down
  if (!rosidl_runtime_c__double__Sequence__are_equal(
      &(lhs->nominal_touch_down), &(rhs->nominal_touch_down)))
  {
    return false;
  }
  // touch_down
  if (!rosidl_runtime_c__double__Sequence__are_equal(
      &(lhs->touch_down), &(rhs->touch_down)))
  {
    return false;
  }
  // swing_period
  if (!rosidl_runtime_c__double__Sequence__are_equal(
      &(lhs->swing_period), &(rhs->swing_period)))
  {
    return false;
  }
  // normal_force_max
  if (!rosidl_runtime_c__double__Sequence__are_equal(
      &(lhs->normal_force_max), &(rhs->normal_force_max)))
  {
    return false;
  }
  // normal_force_min
  if (!rosidl_runtime_c__double__Sequence__are_equal(
      &(lhs->normal_force_min), &(rhs->normal_force_min)))
  {
    return false;
  }
  return true;
}

bool
dls2_interfaces__msg__TrajectoryGenerator__copy(
  const dls2_interfaces__msg__TrajectoryGenerator * input,
  dls2_interfaces__msg__TrajectoryGenerator * output)
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
  // com_pose
  if (!dls2_interfaces__msg__Pose__copy(
      &(input->com_pose), &(output->com_pose)))
  {
    return false;
  }
  // com_vel
  if (!dls2_interfaces__msg__Screw__copy(
      &(input->com_vel), &(output->com_vel)))
  {
    return false;
  }
  // com_acc
  if (!dls2_interfaces__msg__Screw__copy(
      &(input->com_acc), &(output->com_acc)))
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
  // kp
  if (!rosidl_runtime_c__double__Sequence__copy(
      &(input->kp), &(output->kp)))
  {
    return false;
  }
  // kd
  if (!rosidl_runtime_c__double__Sequence__copy(
      &(input->kd), &(output->kd)))
  {
    return false;
  }
  // wrench
  for (size_t i = 0; i < 6; ++i) {
    output->wrench[i] = input->wrench[i];
  }
  // stance_legs
  if (!rosidl_runtime_c__boolean__Sequence__copy(
      &(input->stance_legs), &(output->stance_legs)))
  {
    return false;
  }
  // nominal_touch_down
  if (!rosidl_runtime_c__double__Sequence__copy(
      &(input->nominal_touch_down), &(output->nominal_touch_down)))
  {
    return false;
  }
  // touch_down
  if (!rosidl_runtime_c__double__Sequence__copy(
      &(input->touch_down), &(output->touch_down)))
  {
    return false;
  }
  // swing_period
  if (!rosidl_runtime_c__double__Sequence__copy(
      &(input->swing_period), &(output->swing_period)))
  {
    return false;
  }
  // normal_force_max
  if (!rosidl_runtime_c__double__Sequence__copy(
      &(input->normal_force_max), &(output->normal_force_max)))
  {
    return false;
  }
  // normal_force_min
  if (!rosidl_runtime_c__double__Sequence__copy(
      &(input->normal_force_min), &(output->normal_force_min)))
  {
    return false;
  }
  return true;
}

dls2_interfaces__msg__TrajectoryGenerator *
dls2_interfaces__msg__TrajectoryGenerator__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  dls2_interfaces__msg__TrajectoryGenerator * msg = (dls2_interfaces__msg__TrajectoryGenerator *)allocator.allocate(sizeof(dls2_interfaces__msg__TrajectoryGenerator), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(dls2_interfaces__msg__TrajectoryGenerator));
  bool success = dls2_interfaces__msg__TrajectoryGenerator__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
dls2_interfaces__msg__TrajectoryGenerator__destroy(dls2_interfaces__msg__TrajectoryGenerator * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    dls2_interfaces__msg__TrajectoryGenerator__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
dls2_interfaces__msg__TrajectoryGenerator__Sequence__init(dls2_interfaces__msg__TrajectoryGenerator__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  dls2_interfaces__msg__TrajectoryGenerator * data = NULL;

  if (size) {
    data = (dls2_interfaces__msg__TrajectoryGenerator *)allocator.zero_allocate(size, sizeof(dls2_interfaces__msg__TrajectoryGenerator), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = dls2_interfaces__msg__TrajectoryGenerator__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        dls2_interfaces__msg__TrajectoryGenerator__fini(&data[i - 1]);
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
dls2_interfaces__msg__TrajectoryGenerator__Sequence__fini(dls2_interfaces__msg__TrajectoryGenerator__Sequence * array)
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
      dls2_interfaces__msg__TrajectoryGenerator__fini(&array->data[i]);
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

dls2_interfaces__msg__TrajectoryGenerator__Sequence *
dls2_interfaces__msg__TrajectoryGenerator__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  dls2_interfaces__msg__TrajectoryGenerator__Sequence * array = (dls2_interfaces__msg__TrajectoryGenerator__Sequence *)allocator.allocate(sizeof(dls2_interfaces__msg__TrajectoryGenerator__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = dls2_interfaces__msg__TrajectoryGenerator__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
dls2_interfaces__msg__TrajectoryGenerator__Sequence__destroy(dls2_interfaces__msg__TrajectoryGenerator__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    dls2_interfaces__msg__TrajectoryGenerator__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
dls2_interfaces__msg__TrajectoryGenerator__Sequence__are_equal(const dls2_interfaces__msg__TrajectoryGenerator__Sequence * lhs, const dls2_interfaces__msg__TrajectoryGenerator__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!dls2_interfaces__msg__TrajectoryGenerator__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
dls2_interfaces__msg__TrajectoryGenerator__Sequence__copy(
  const dls2_interfaces__msg__TrajectoryGenerator__Sequence * input,
  dls2_interfaces__msg__TrajectoryGenerator__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(dls2_interfaces__msg__TrajectoryGenerator);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    dls2_interfaces__msg__TrajectoryGenerator * data =
      (dls2_interfaces__msg__TrajectoryGenerator *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!dls2_interfaces__msg__TrajectoryGenerator__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          dls2_interfaces__msg__TrajectoryGenerator__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!dls2_interfaces__msg__TrajectoryGenerator__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
