// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from dls2_interfaces:msg/BaseState.idl
// generated code does not contain a copyright notice

#ifndef DLS2_INTERFACES__MSG__DETAIL__BASE_STATE__TRAITS_HPP_
#define DLS2_INTERFACES__MSG__DETAIL__BASE_STATE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "dls2_interfaces/msg/detail/base_state__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'pose'
#include "dls2_interfaces/msg/detail/pose__traits.hpp"
// Member 'velocity'
// Member 'acceleration'
#include "dls2_interfaces/msg/detail/screw__traits.hpp"

namespace dls2_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const BaseState & msg,
  std::ostream & out)
{
  out << "{";
  // member: frame_id
  {
    out << "frame_id: ";
    rosidl_generator_traits::value_to_yaml(msg.frame_id, out);
    out << ", ";
  }

  // member: sequence_id
  {
    out << "sequence_id: ";
    rosidl_generator_traits::value_to_yaml(msg.sequence_id, out);
    out << ", ";
  }

  // member: timestamp
  {
    out << "timestamp: ";
    rosidl_generator_traits::value_to_yaml(msg.timestamp, out);
    out << ", ";
  }

  // member: robot_name
  {
    out << "robot_name: ";
    rosidl_generator_traits::value_to_yaml(msg.robot_name, out);
    out << ", ";
  }

  // member: pose
  {
    out << "pose: ";
    to_flow_style_yaml(msg.pose, out);
    out << ", ";
  }

  // member: velocity
  {
    out << "velocity: ";
    to_flow_style_yaml(msg.velocity, out);
    out << ", ";
  }

  // member: acceleration
  {
    out << "acceleration: ";
    to_flow_style_yaml(msg.acceleration, out);
    out << ", ";
  }

  // member: stance_status
  {
    if (msg.stance_status.size() == 0) {
      out << "stance_status: []";
    } else {
      out << "stance_status: [";
      size_t pending_items = msg.stance_status.size();
      for (auto item : msg.stance_status) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const BaseState & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: frame_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "frame_id: ";
    rosidl_generator_traits::value_to_yaml(msg.frame_id, out);
    out << "\n";
  }

  // member: sequence_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "sequence_id: ";
    rosidl_generator_traits::value_to_yaml(msg.sequence_id, out);
    out << "\n";
  }

  // member: timestamp
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "timestamp: ";
    rosidl_generator_traits::value_to_yaml(msg.timestamp, out);
    out << "\n";
  }

  // member: robot_name
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "robot_name: ";
    rosidl_generator_traits::value_to_yaml(msg.robot_name, out);
    out << "\n";
  }

  // member: pose
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "pose:\n";
    to_block_style_yaml(msg.pose, out, indentation + 2);
  }

  // member: velocity
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "velocity:\n";
    to_block_style_yaml(msg.velocity, out, indentation + 2);
  }

  // member: acceleration
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "acceleration:\n";
    to_block_style_yaml(msg.acceleration, out, indentation + 2);
  }

  // member: stance_status
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.stance_status.size() == 0) {
      out << "stance_status: []\n";
    } else {
      out << "stance_status:\n";
      for (auto item : msg.stance_status) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const BaseState & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace dls2_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use dls2_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const dls2_interfaces::msg::BaseState & msg,
  std::ostream & out, size_t indentation = 0)
{
  dls2_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use dls2_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const dls2_interfaces::msg::BaseState & msg)
{
  return dls2_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<dls2_interfaces::msg::BaseState>()
{
  return "dls2_interfaces::msg::BaseState";
}

template<>
inline const char * name<dls2_interfaces::msg::BaseState>()
{
  return "dls2_interfaces/msg/BaseState";
}

template<>
struct has_fixed_size<dls2_interfaces::msg::BaseState>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<dls2_interfaces::msg::BaseState>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<dls2_interfaces::msg::BaseState>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // DLS2_INTERFACES__MSG__DETAIL__BASE_STATE__TRAITS_HPP_
