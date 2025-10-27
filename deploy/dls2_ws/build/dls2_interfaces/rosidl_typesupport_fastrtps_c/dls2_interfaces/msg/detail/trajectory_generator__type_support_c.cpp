// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from dls2_interfaces:msg/TrajectoryGenerator.idl
// generated code does not contain a copyright notice
#include "dls2_interfaces/msg/detail/trajectory_generator__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "dls2_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "dls2_interfaces/msg/detail/trajectory_generator__struct.h"
#include "dls2_interfaces/msg/detail/trajectory_generator__functions.h"
#include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif

#include "dls2_interfaces/msg/detail/pose__functions.h"  // com_pose
#include "dls2_interfaces/msg/detail/screw__functions.h"  // com_acc, com_vel
#include "rosidl_runtime_c/primitives_sequence.h"  // joints_acceleration, joints_effort, joints_position, joints_velocity, kd, kp, nominal_touch_down, normal_force_max, normal_force_min, stance_legs, swing_period, touch_down
#include "rosidl_runtime_c/primitives_sequence_functions.h"  // joints_acceleration, joints_effort, joints_position, joints_velocity, kd, kp, nominal_touch_down, normal_force_max, normal_force_min, stance_legs, swing_period, touch_down
#include "rosidl_runtime_c/string.h"  // frame_id
#include "rosidl_runtime_c/string_functions.h"  // frame_id

// forward declare type support functions
size_t get_serialized_size_dls2_interfaces__msg__Pose(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_dls2_interfaces__msg__Pose(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, dls2_interfaces, msg, Pose)();
size_t get_serialized_size_dls2_interfaces__msg__Screw(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_dls2_interfaces__msg__Screw(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, dls2_interfaces, msg, Screw)();


using _TrajectoryGenerator__ros_msg_type = dls2_interfaces__msg__TrajectoryGenerator;

static bool _TrajectoryGenerator__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _TrajectoryGenerator__ros_msg_type * ros_message = static_cast<const _TrajectoryGenerator__ros_msg_type *>(untyped_ros_message);
  // Field name: frame_id
  {
    const rosidl_runtime_c__String * str = &ros_message->frame_id;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: sequence_id
  {
    cdr << ros_message->sequence_id;
  }

  // Field name: timestamp
  {
    cdr << ros_message->timestamp;
  }

  // Field name: com_pose
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, dls2_interfaces, msg, Pose
      )()->data);
    if (!callbacks->cdr_serialize(
        &ros_message->com_pose, cdr))
    {
      return false;
    }
  }

  // Field name: com_vel
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, dls2_interfaces, msg, Screw
      )()->data);
    if (!callbacks->cdr_serialize(
        &ros_message->com_vel, cdr))
    {
      return false;
    }
  }

  // Field name: com_acc
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, dls2_interfaces, msg, Screw
      )()->data);
    if (!callbacks->cdr_serialize(
        &ros_message->com_acc, cdr))
    {
      return false;
    }
  }

  // Field name: joints_position
  {
    size_t size = ros_message->joints_position.size;
    auto array_ptr = ros_message->joints_position.data;
    cdr << static_cast<uint32_t>(size);
    cdr.serializeArray(array_ptr, size);
  }

  // Field name: joints_velocity
  {
    size_t size = ros_message->joints_velocity.size;
    auto array_ptr = ros_message->joints_velocity.data;
    cdr << static_cast<uint32_t>(size);
    cdr.serializeArray(array_ptr, size);
  }

  // Field name: joints_acceleration
  {
    size_t size = ros_message->joints_acceleration.size;
    auto array_ptr = ros_message->joints_acceleration.data;
    cdr << static_cast<uint32_t>(size);
    cdr.serializeArray(array_ptr, size);
  }

  // Field name: joints_effort
  {
    size_t size = ros_message->joints_effort.size;
    auto array_ptr = ros_message->joints_effort.data;
    cdr << static_cast<uint32_t>(size);
    cdr.serializeArray(array_ptr, size);
  }

  // Field name: kp
  {
    size_t size = ros_message->kp.size;
    auto array_ptr = ros_message->kp.data;
    cdr << static_cast<uint32_t>(size);
    cdr.serializeArray(array_ptr, size);
  }

  // Field name: kd
  {
    size_t size = ros_message->kd.size;
    auto array_ptr = ros_message->kd.data;
    cdr << static_cast<uint32_t>(size);
    cdr.serializeArray(array_ptr, size);
  }

  // Field name: wrench
  {
    size_t size = 6;
    auto array_ptr = ros_message->wrench;
    cdr.serializeArray(array_ptr, size);
  }

  // Field name: stance_legs
  {
    size_t size = ros_message->stance_legs.size;
    auto array_ptr = ros_message->stance_legs.data;
    cdr << static_cast<uint32_t>(size);
    cdr.serializeArray(array_ptr, size);
  }

  // Field name: nominal_touch_down
  {
    size_t size = ros_message->nominal_touch_down.size;
    auto array_ptr = ros_message->nominal_touch_down.data;
    cdr << static_cast<uint32_t>(size);
    cdr.serializeArray(array_ptr, size);
  }

  // Field name: touch_down
  {
    size_t size = ros_message->touch_down.size;
    auto array_ptr = ros_message->touch_down.data;
    cdr << static_cast<uint32_t>(size);
    cdr.serializeArray(array_ptr, size);
  }

  // Field name: swing_period
  {
    size_t size = ros_message->swing_period.size;
    auto array_ptr = ros_message->swing_period.data;
    cdr << static_cast<uint32_t>(size);
    cdr.serializeArray(array_ptr, size);
  }

  // Field name: normal_force_max
  {
    size_t size = ros_message->normal_force_max.size;
    auto array_ptr = ros_message->normal_force_max.data;
    cdr << static_cast<uint32_t>(size);
    cdr.serializeArray(array_ptr, size);
  }

  // Field name: normal_force_min
  {
    size_t size = ros_message->normal_force_min.size;
    auto array_ptr = ros_message->normal_force_min.data;
    cdr << static_cast<uint32_t>(size);
    cdr.serializeArray(array_ptr, size);
  }

  return true;
}

static bool _TrajectoryGenerator__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _TrajectoryGenerator__ros_msg_type * ros_message = static_cast<_TrajectoryGenerator__ros_msg_type *>(untyped_ros_message);
  // Field name: frame_id
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->frame_id.data) {
      rosidl_runtime_c__String__init(&ros_message->frame_id);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->frame_id,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'frame_id'\n");
      return false;
    }
  }

  // Field name: sequence_id
  {
    cdr >> ros_message->sequence_id;
  }

  // Field name: timestamp
  {
    cdr >> ros_message->timestamp;
  }

  // Field name: com_pose
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, dls2_interfaces, msg, Pose
      )()->data);
    if (!callbacks->cdr_deserialize(
        cdr, &ros_message->com_pose))
    {
      return false;
    }
  }

  // Field name: com_vel
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, dls2_interfaces, msg, Screw
      )()->data);
    if (!callbacks->cdr_deserialize(
        cdr, &ros_message->com_vel))
    {
      return false;
    }
  }

  // Field name: com_acc
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, dls2_interfaces, msg, Screw
      )()->data);
    if (!callbacks->cdr_deserialize(
        cdr, &ros_message->com_acc))
    {
      return false;
    }
  }

  // Field name: joints_position
  {
    uint32_t cdrSize;
    cdr >> cdrSize;
    size_t size = static_cast<size_t>(cdrSize);
    if (ros_message->joints_position.data) {
      rosidl_runtime_c__double__Sequence__fini(&ros_message->joints_position);
    }
    if (!rosidl_runtime_c__double__Sequence__init(&ros_message->joints_position, size)) {
      fprintf(stderr, "failed to create array for field 'joints_position'");
      return false;
    }
    auto array_ptr = ros_message->joints_position.data;
    cdr.deserializeArray(array_ptr, size);
  }

  // Field name: joints_velocity
  {
    uint32_t cdrSize;
    cdr >> cdrSize;
    size_t size = static_cast<size_t>(cdrSize);
    if (ros_message->joints_velocity.data) {
      rosidl_runtime_c__double__Sequence__fini(&ros_message->joints_velocity);
    }
    if (!rosidl_runtime_c__double__Sequence__init(&ros_message->joints_velocity, size)) {
      fprintf(stderr, "failed to create array for field 'joints_velocity'");
      return false;
    }
    auto array_ptr = ros_message->joints_velocity.data;
    cdr.deserializeArray(array_ptr, size);
  }

  // Field name: joints_acceleration
  {
    uint32_t cdrSize;
    cdr >> cdrSize;
    size_t size = static_cast<size_t>(cdrSize);
    if (ros_message->joints_acceleration.data) {
      rosidl_runtime_c__double__Sequence__fini(&ros_message->joints_acceleration);
    }
    if (!rosidl_runtime_c__double__Sequence__init(&ros_message->joints_acceleration, size)) {
      fprintf(stderr, "failed to create array for field 'joints_acceleration'");
      return false;
    }
    auto array_ptr = ros_message->joints_acceleration.data;
    cdr.deserializeArray(array_ptr, size);
  }

  // Field name: joints_effort
  {
    uint32_t cdrSize;
    cdr >> cdrSize;
    size_t size = static_cast<size_t>(cdrSize);
    if (ros_message->joints_effort.data) {
      rosidl_runtime_c__double__Sequence__fini(&ros_message->joints_effort);
    }
    if (!rosidl_runtime_c__double__Sequence__init(&ros_message->joints_effort, size)) {
      fprintf(stderr, "failed to create array for field 'joints_effort'");
      return false;
    }
    auto array_ptr = ros_message->joints_effort.data;
    cdr.deserializeArray(array_ptr, size);
  }

  // Field name: kp
  {
    uint32_t cdrSize;
    cdr >> cdrSize;
    size_t size = static_cast<size_t>(cdrSize);
    if (ros_message->kp.data) {
      rosidl_runtime_c__double__Sequence__fini(&ros_message->kp);
    }
    if (!rosidl_runtime_c__double__Sequence__init(&ros_message->kp, size)) {
      fprintf(stderr, "failed to create array for field 'kp'");
      return false;
    }
    auto array_ptr = ros_message->kp.data;
    cdr.deserializeArray(array_ptr, size);
  }

  // Field name: kd
  {
    uint32_t cdrSize;
    cdr >> cdrSize;
    size_t size = static_cast<size_t>(cdrSize);
    if (ros_message->kd.data) {
      rosidl_runtime_c__double__Sequence__fini(&ros_message->kd);
    }
    if (!rosidl_runtime_c__double__Sequence__init(&ros_message->kd, size)) {
      fprintf(stderr, "failed to create array for field 'kd'");
      return false;
    }
    auto array_ptr = ros_message->kd.data;
    cdr.deserializeArray(array_ptr, size);
  }

  // Field name: wrench
  {
    size_t size = 6;
    auto array_ptr = ros_message->wrench;
    cdr.deserializeArray(array_ptr, size);
  }

  // Field name: stance_legs
  {
    uint32_t cdrSize;
    cdr >> cdrSize;
    size_t size = static_cast<size_t>(cdrSize);
    if (ros_message->stance_legs.data) {
      rosidl_runtime_c__boolean__Sequence__fini(&ros_message->stance_legs);
    }
    if (!rosidl_runtime_c__boolean__Sequence__init(&ros_message->stance_legs, size)) {
      fprintf(stderr, "failed to create array for field 'stance_legs'");
      return false;
    }
    auto array_ptr = ros_message->stance_legs.data;
    for (size_t i = 0; i < size; ++i) {
      uint8_t tmp;
      cdr >> tmp;
      array_ptr[i] = tmp ? true : false;
    }
  }

  // Field name: nominal_touch_down
  {
    uint32_t cdrSize;
    cdr >> cdrSize;
    size_t size = static_cast<size_t>(cdrSize);
    if (ros_message->nominal_touch_down.data) {
      rosidl_runtime_c__double__Sequence__fini(&ros_message->nominal_touch_down);
    }
    if (!rosidl_runtime_c__double__Sequence__init(&ros_message->nominal_touch_down, size)) {
      fprintf(stderr, "failed to create array for field 'nominal_touch_down'");
      return false;
    }
    auto array_ptr = ros_message->nominal_touch_down.data;
    cdr.deserializeArray(array_ptr, size);
  }

  // Field name: touch_down
  {
    uint32_t cdrSize;
    cdr >> cdrSize;
    size_t size = static_cast<size_t>(cdrSize);
    if (ros_message->touch_down.data) {
      rosidl_runtime_c__double__Sequence__fini(&ros_message->touch_down);
    }
    if (!rosidl_runtime_c__double__Sequence__init(&ros_message->touch_down, size)) {
      fprintf(stderr, "failed to create array for field 'touch_down'");
      return false;
    }
    auto array_ptr = ros_message->touch_down.data;
    cdr.deserializeArray(array_ptr, size);
  }

  // Field name: swing_period
  {
    uint32_t cdrSize;
    cdr >> cdrSize;
    size_t size = static_cast<size_t>(cdrSize);
    if (ros_message->swing_period.data) {
      rosidl_runtime_c__double__Sequence__fini(&ros_message->swing_period);
    }
    if (!rosidl_runtime_c__double__Sequence__init(&ros_message->swing_period, size)) {
      fprintf(stderr, "failed to create array for field 'swing_period'");
      return false;
    }
    auto array_ptr = ros_message->swing_period.data;
    cdr.deserializeArray(array_ptr, size);
  }

  // Field name: normal_force_max
  {
    uint32_t cdrSize;
    cdr >> cdrSize;
    size_t size = static_cast<size_t>(cdrSize);
    if (ros_message->normal_force_max.data) {
      rosidl_runtime_c__double__Sequence__fini(&ros_message->normal_force_max);
    }
    if (!rosidl_runtime_c__double__Sequence__init(&ros_message->normal_force_max, size)) {
      fprintf(stderr, "failed to create array for field 'normal_force_max'");
      return false;
    }
    auto array_ptr = ros_message->normal_force_max.data;
    cdr.deserializeArray(array_ptr, size);
  }

  // Field name: normal_force_min
  {
    uint32_t cdrSize;
    cdr >> cdrSize;
    size_t size = static_cast<size_t>(cdrSize);
    if (ros_message->normal_force_min.data) {
      rosidl_runtime_c__double__Sequence__fini(&ros_message->normal_force_min);
    }
    if (!rosidl_runtime_c__double__Sequence__init(&ros_message->normal_force_min, size)) {
      fprintf(stderr, "failed to create array for field 'normal_force_min'");
      return false;
    }
    auto array_ptr = ros_message->normal_force_min.data;
    cdr.deserializeArray(array_ptr, size);
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_dls2_interfaces
size_t get_serialized_size_dls2_interfaces__msg__TrajectoryGenerator(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _TrajectoryGenerator__ros_msg_type * ros_message = static_cast<const _TrajectoryGenerator__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name frame_id
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->frame_id.size + 1);
  // field.name sequence_id
  {
    size_t item_size = sizeof(ros_message->sequence_id);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name timestamp
  {
    size_t item_size = sizeof(ros_message->timestamp);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name com_pose

  current_alignment += get_serialized_size_dls2_interfaces__msg__Pose(
    &(ros_message->com_pose), current_alignment);
  // field.name com_vel

  current_alignment += get_serialized_size_dls2_interfaces__msg__Screw(
    &(ros_message->com_vel), current_alignment);
  // field.name com_acc

  current_alignment += get_serialized_size_dls2_interfaces__msg__Screw(
    &(ros_message->com_acc), current_alignment);
  // field.name joints_position
  {
    size_t array_size = ros_message->joints_position.size;
    auto array_ptr = ros_message->joints_position.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    (void)array_ptr;
    size_t item_size = sizeof(array_ptr[0]);
    current_alignment += array_size * item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name joints_velocity
  {
    size_t array_size = ros_message->joints_velocity.size;
    auto array_ptr = ros_message->joints_velocity.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    (void)array_ptr;
    size_t item_size = sizeof(array_ptr[0]);
    current_alignment += array_size * item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name joints_acceleration
  {
    size_t array_size = ros_message->joints_acceleration.size;
    auto array_ptr = ros_message->joints_acceleration.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    (void)array_ptr;
    size_t item_size = sizeof(array_ptr[0]);
    current_alignment += array_size * item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name joints_effort
  {
    size_t array_size = ros_message->joints_effort.size;
    auto array_ptr = ros_message->joints_effort.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    (void)array_ptr;
    size_t item_size = sizeof(array_ptr[0]);
    current_alignment += array_size * item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name kp
  {
    size_t array_size = ros_message->kp.size;
    auto array_ptr = ros_message->kp.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    (void)array_ptr;
    size_t item_size = sizeof(array_ptr[0]);
    current_alignment += array_size * item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name kd
  {
    size_t array_size = ros_message->kd.size;
    auto array_ptr = ros_message->kd.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    (void)array_ptr;
    size_t item_size = sizeof(array_ptr[0]);
    current_alignment += array_size * item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name wrench
  {
    size_t array_size = 6;
    auto array_ptr = ros_message->wrench;
    (void)array_ptr;
    size_t item_size = sizeof(array_ptr[0]);
    current_alignment += array_size * item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name stance_legs
  {
    size_t array_size = ros_message->stance_legs.size;
    auto array_ptr = ros_message->stance_legs.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    (void)array_ptr;
    size_t item_size = sizeof(array_ptr[0]);
    current_alignment += array_size * item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name nominal_touch_down
  {
    size_t array_size = ros_message->nominal_touch_down.size;
    auto array_ptr = ros_message->nominal_touch_down.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    (void)array_ptr;
    size_t item_size = sizeof(array_ptr[0]);
    current_alignment += array_size * item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name touch_down
  {
    size_t array_size = ros_message->touch_down.size;
    auto array_ptr = ros_message->touch_down.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    (void)array_ptr;
    size_t item_size = sizeof(array_ptr[0]);
    current_alignment += array_size * item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name swing_period
  {
    size_t array_size = ros_message->swing_period.size;
    auto array_ptr = ros_message->swing_period.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    (void)array_ptr;
    size_t item_size = sizeof(array_ptr[0]);
    current_alignment += array_size * item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name normal_force_max
  {
    size_t array_size = ros_message->normal_force_max.size;
    auto array_ptr = ros_message->normal_force_max.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    (void)array_ptr;
    size_t item_size = sizeof(array_ptr[0]);
    current_alignment += array_size * item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name normal_force_min
  {
    size_t array_size = ros_message->normal_force_min.size;
    auto array_ptr = ros_message->normal_force_min.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    (void)array_ptr;
    size_t item_size = sizeof(array_ptr[0]);
    current_alignment += array_size * item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

static uint32_t _TrajectoryGenerator__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_dls2_interfaces__msg__TrajectoryGenerator(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_dls2_interfaces
size_t max_serialized_size_dls2_interfaces__msg__TrajectoryGenerator(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // member: frame_id
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: sequence_id
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }
  // member: timestamp
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: com_pose
  {
    size_t array_size = 1;


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_dls2_interfaces__msg__Pose(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }
  // member: com_vel
  {
    size_t array_size = 1;


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_dls2_interfaces__msg__Screw(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }
  // member: com_acc
  {
    size_t array_size = 1;


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_dls2_interfaces__msg__Screw(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }
  // member: joints_position
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: joints_velocity
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: joints_acceleration
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: joints_effort
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: kp
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: kd
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: wrench
  {
    size_t array_size = 6;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: stance_legs
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: nominal_touch_down
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: touch_down
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: swing_period
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: normal_force_max
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: normal_force_min
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = dls2_interfaces__msg__TrajectoryGenerator;
    is_plain =
      (
      offsetof(DataType, normal_force_min) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _TrajectoryGenerator__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_dls2_interfaces__msg__TrajectoryGenerator(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_TrajectoryGenerator = {
  "dls2_interfaces::msg",
  "TrajectoryGenerator",
  _TrajectoryGenerator__cdr_serialize,
  _TrajectoryGenerator__cdr_deserialize,
  _TrajectoryGenerator__get_serialized_size,
  _TrajectoryGenerator__max_serialized_size
};

static rosidl_message_type_support_t _TrajectoryGenerator__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_TrajectoryGenerator,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, dls2_interfaces, msg, TrajectoryGenerator)() {
  return &_TrajectoryGenerator__type_support;
}

#if defined(__cplusplus)
}
#endif
