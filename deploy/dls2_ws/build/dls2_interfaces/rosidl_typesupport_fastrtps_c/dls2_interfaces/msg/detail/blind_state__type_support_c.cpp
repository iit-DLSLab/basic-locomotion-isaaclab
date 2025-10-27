// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from dls2_interfaces:msg/BlindState.idl
// generated code does not contain a copyright notice
#include "dls2_interfaces/msg/detail/blind_state__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "dls2_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "dls2_interfaces/msg/detail/blind_state__struct.h"
#include "dls2_interfaces/msg/detail/blind_state__functions.h"
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

#include "rosidl_runtime_c/primitives_sequence.h"  // current_feet_positions, feet_contact, joints_acceleration, joints_effort, joints_position, joints_temperature, joints_velocity
#include "rosidl_runtime_c/primitives_sequence_functions.h"  // current_feet_positions, feet_contact, joints_acceleration, joints_effort, joints_position, joints_temperature, joints_velocity
#include "rosidl_runtime_c/string.h"  // frame_id, joints_name, robot_name
#include "rosidl_runtime_c/string_functions.h"  // frame_id, joints_name, robot_name

// forward declare type support functions


using _BlindState__ros_msg_type = dls2_interfaces__msg__BlindState;

static bool _BlindState__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _BlindState__ros_msg_type * ros_message = static_cast<const _BlindState__ros_msg_type *>(untyped_ros_message);
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

  // Field name: robot_name
  {
    const rosidl_runtime_c__String * str = &ros_message->robot_name;
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

  // Field name: joints_name
  {
    size_t size = ros_message->joints_name.size;
    auto array_ptr = ros_message->joints_name.data;
    cdr << static_cast<uint32_t>(size);
    for (size_t i = 0; i < size; ++i) {
      const rosidl_runtime_c__String * str = &array_ptr[i];
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

  // Field name: joints_temperature
  {
    size_t size = ros_message->joints_temperature.size;
    auto array_ptr = ros_message->joints_temperature.data;
    cdr << static_cast<uint32_t>(size);
    cdr.serializeArray(array_ptr, size);
  }

  // Field name: feet_contact
  {
    size_t size = ros_message->feet_contact.size;
    auto array_ptr = ros_message->feet_contact.data;
    cdr << static_cast<uint32_t>(size);
    cdr.serializeArray(array_ptr, size);
  }

  // Field name: current_feet_positions
  {
    size_t size = ros_message->current_feet_positions.size;
    auto array_ptr = ros_message->current_feet_positions.data;
    cdr << static_cast<uint32_t>(size);
    cdr.serializeArray(array_ptr, size);
  }

  return true;
}

static bool _BlindState__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _BlindState__ros_msg_type * ros_message = static_cast<_BlindState__ros_msg_type *>(untyped_ros_message);
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

  // Field name: robot_name
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->robot_name.data) {
      rosidl_runtime_c__String__init(&ros_message->robot_name);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->robot_name,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'robot_name'\n");
      return false;
    }
  }

  // Field name: joints_name
  {
    uint32_t cdrSize;
    cdr >> cdrSize;
    size_t size = static_cast<size_t>(cdrSize);
    if (ros_message->joints_name.data) {
      rosidl_runtime_c__String__Sequence__fini(&ros_message->joints_name);
    }
    if (!rosidl_runtime_c__String__Sequence__init(&ros_message->joints_name, size)) {
      fprintf(stderr, "failed to create array for field 'joints_name'");
      return false;
    }
    auto array_ptr = ros_message->joints_name.data;
    for (size_t i = 0; i < size; ++i) {
      std::string tmp;
      cdr >> tmp;
      auto & ros_i = array_ptr[i];
      if (!ros_i.data) {
        rosidl_runtime_c__String__init(&ros_i);
      }
      bool succeeded = rosidl_runtime_c__String__assign(
        &ros_i,
        tmp.c_str());
      if (!succeeded) {
        fprintf(stderr, "failed to assign string into field 'joints_name'\n");
        return false;
      }
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

  // Field name: joints_temperature
  {
    uint32_t cdrSize;
    cdr >> cdrSize;
    size_t size = static_cast<size_t>(cdrSize);
    if (ros_message->joints_temperature.data) {
      rosidl_runtime_c__double__Sequence__fini(&ros_message->joints_temperature);
    }
    if (!rosidl_runtime_c__double__Sequence__init(&ros_message->joints_temperature, size)) {
      fprintf(stderr, "failed to create array for field 'joints_temperature'");
      return false;
    }
    auto array_ptr = ros_message->joints_temperature.data;
    cdr.deserializeArray(array_ptr, size);
  }

  // Field name: feet_contact
  {
    uint32_t cdrSize;
    cdr >> cdrSize;
    size_t size = static_cast<size_t>(cdrSize);
    if (ros_message->feet_contact.data) {
      rosidl_runtime_c__boolean__Sequence__fini(&ros_message->feet_contact);
    }
    if (!rosidl_runtime_c__boolean__Sequence__init(&ros_message->feet_contact, size)) {
      fprintf(stderr, "failed to create array for field 'feet_contact'");
      return false;
    }
    auto array_ptr = ros_message->feet_contact.data;
    for (size_t i = 0; i < size; ++i) {
      uint8_t tmp;
      cdr >> tmp;
      array_ptr[i] = tmp ? true : false;
    }
  }

  // Field name: current_feet_positions
  {
    uint32_t cdrSize;
    cdr >> cdrSize;
    size_t size = static_cast<size_t>(cdrSize);
    if (ros_message->current_feet_positions.data) {
      rosidl_runtime_c__double__Sequence__fini(&ros_message->current_feet_positions);
    }
    if (!rosidl_runtime_c__double__Sequence__init(&ros_message->current_feet_positions, size)) {
      fprintf(stderr, "failed to create array for field 'current_feet_positions'");
      return false;
    }
    auto array_ptr = ros_message->current_feet_positions.data;
    cdr.deserializeArray(array_ptr, size);
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_dls2_interfaces
size_t get_serialized_size_dls2_interfaces__msg__BlindState(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _BlindState__ros_msg_type * ros_message = static_cast<const _BlindState__ros_msg_type *>(untyped_ros_message);
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
  // field.name robot_name
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->robot_name.size + 1);
  // field.name joints_name
  {
    size_t array_size = ros_message->joints_name.size;
    auto array_ptr = ros_message->joints_name.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        (array_ptr[index].size + 1);
    }
  }
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
  // field.name joints_temperature
  {
    size_t array_size = ros_message->joints_temperature.size;
    auto array_ptr = ros_message->joints_temperature.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    (void)array_ptr;
    size_t item_size = sizeof(array_ptr[0]);
    current_alignment += array_size * item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name feet_contact
  {
    size_t array_size = ros_message->feet_contact.size;
    auto array_ptr = ros_message->feet_contact.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    (void)array_ptr;
    size_t item_size = sizeof(array_ptr[0]);
    current_alignment += array_size * item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name current_feet_positions
  {
    size_t array_size = ros_message->current_feet_positions.size;
    auto array_ptr = ros_message->current_feet_positions.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    (void)array_ptr;
    size_t item_size = sizeof(array_ptr[0]);
    current_alignment += array_size * item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

static uint32_t _BlindState__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_dls2_interfaces__msg__BlindState(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_dls2_interfaces
size_t max_serialized_size_dls2_interfaces__msg__BlindState(
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
  // member: robot_name
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
  // member: joints_name
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
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
  // member: joints_temperature
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
  // member: feet_contact
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: current_feet_positions
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
    using DataType = dls2_interfaces__msg__BlindState;
    is_plain =
      (
      offsetof(DataType, current_feet_positions) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _BlindState__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_dls2_interfaces__msg__BlindState(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_BlindState = {
  "dls2_interfaces::msg",
  "BlindState",
  _BlindState__cdr_serialize,
  _BlindState__cdr_deserialize,
  _BlindState__get_serialized_size,
  _BlindState__max_serialized_size
};

static rosidl_message_type_support_t _BlindState__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_BlindState,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, dls2_interfaces, msg, BlindState)() {
  return &_BlindState__type_support;
}

#if defined(__cplusplus)
}
#endif
