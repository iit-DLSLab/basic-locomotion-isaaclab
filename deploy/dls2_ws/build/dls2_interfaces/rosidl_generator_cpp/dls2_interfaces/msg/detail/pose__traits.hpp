// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from dls2_interfaces:msg/Pose.idl
// generated code does not contain a copyright notice

#ifndef DLS2_INTERFACES__MSG__DETAIL__POSE__TRAITS_HPP_
#define DLS2_INTERFACES__MSG__DETAIL__POSE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "dls2_interfaces/msg/detail/pose__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace dls2_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const Pose & msg,
  std::ostream & out)
{
  out << "{";
  // member: position
  {
    if (msg.position.size() == 0) {
      out << "position: []";
    } else {
      out << "position: [";
      size_t pending_items = msg.position.size();
      for (auto item : msg.position) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: orientation
  {
    if (msg.orientation.size() == 0) {
      out << "orientation: []";
    } else {
      out << "orientation: [";
      size_t pending_items = msg.orientation.size();
      for (auto item : msg.orientation) {
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
  const Pose & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: position
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.position.size() == 0) {
      out << "position: []\n";
    } else {
      out << "position:\n";
      for (auto item : msg.position) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: orientation
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.orientation.size() == 0) {
      out << "orientation: []\n";
    } else {
      out << "orientation:\n";
      for (auto item : msg.orientation) {
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

inline std::string to_yaml(const Pose & msg, bool use_flow_style = false)
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
  const dls2_interfaces::msg::Pose & msg,
  std::ostream & out, size_t indentation = 0)
{
  dls2_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use dls2_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const dls2_interfaces::msg::Pose & msg)
{
  return dls2_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<dls2_interfaces::msg::Pose>()
{
  return "dls2_interfaces::msg::Pose";
}

template<>
inline const char * name<dls2_interfaces::msg::Pose>()
{
  return "dls2_interfaces/msg/Pose";
}

template<>
struct has_fixed_size<dls2_interfaces::msg::Pose>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<dls2_interfaces::msg::Pose>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<dls2_interfaces::msg::Pose>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // DLS2_INTERFACES__MSG__DETAIL__POSE__TRAITS_HPP_
