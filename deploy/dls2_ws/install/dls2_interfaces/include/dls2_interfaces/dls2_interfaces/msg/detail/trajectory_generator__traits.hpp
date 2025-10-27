// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from dls2_interfaces:msg/TrajectoryGenerator.idl
// generated code does not contain a copyright notice

#ifndef DLS2_INTERFACES__MSG__DETAIL__TRAJECTORY_GENERATOR__TRAITS_HPP_
#define DLS2_INTERFACES__MSG__DETAIL__TRAJECTORY_GENERATOR__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "dls2_interfaces/msg/detail/trajectory_generator__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'com_pose'
#include "dls2_interfaces/msg/detail/pose__traits.hpp"
// Member 'com_vel'
// Member 'com_acc'
#include "dls2_interfaces/msg/detail/screw__traits.hpp"

namespace dls2_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const TrajectoryGenerator & msg,
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

  // member: com_pose
  {
    out << "com_pose: ";
    to_flow_style_yaml(msg.com_pose, out);
    out << ", ";
  }

  // member: com_vel
  {
    out << "com_vel: ";
    to_flow_style_yaml(msg.com_vel, out);
    out << ", ";
  }

  // member: com_acc
  {
    out << "com_acc: ";
    to_flow_style_yaml(msg.com_acc, out);
    out << ", ";
  }

  // member: joints_position
  {
    if (msg.joints_position.size() == 0) {
      out << "joints_position: []";
    } else {
      out << "joints_position: [";
      size_t pending_items = msg.joints_position.size();
      for (auto item : msg.joints_position) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: joints_velocity
  {
    if (msg.joints_velocity.size() == 0) {
      out << "joints_velocity: []";
    } else {
      out << "joints_velocity: [";
      size_t pending_items = msg.joints_velocity.size();
      for (auto item : msg.joints_velocity) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: joints_acceleration
  {
    if (msg.joints_acceleration.size() == 0) {
      out << "joints_acceleration: []";
    } else {
      out << "joints_acceleration: [";
      size_t pending_items = msg.joints_acceleration.size();
      for (auto item : msg.joints_acceleration) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: joints_effort
  {
    if (msg.joints_effort.size() == 0) {
      out << "joints_effort: []";
    } else {
      out << "joints_effort: [";
      size_t pending_items = msg.joints_effort.size();
      for (auto item : msg.joints_effort) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: kp
  {
    if (msg.kp.size() == 0) {
      out << "kp: []";
    } else {
      out << "kp: [";
      size_t pending_items = msg.kp.size();
      for (auto item : msg.kp) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: kd
  {
    if (msg.kd.size() == 0) {
      out << "kd: []";
    } else {
      out << "kd: [";
      size_t pending_items = msg.kd.size();
      for (auto item : msg.kd) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: wrench
  {
    if (msg.wrench.size() == 0) {
      out << "wrench: []";
    } else {
      out << "wrench: [";
      size_t pending_items = msg.wrench.size();
      for (auto item : msg.wrench) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: stance_legs
  {
    if (msg.stance_legs.size() == 0) {
      out << "stance_legs: []";
    } else {
      out << "stance_legs: [";
      size_t pending_items = msg.stance_legs.size();
      for (auto item : msg.stance_legs) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: nominal_touch_down
  {
    if (msg.nominal_touch_down.size() == 0) {
      out << "nominal_touch_down: []";
    } else {
      out << "nominal_touch_down: [";
      size_t pending_items = msg.nominal_touch_down.size();
      for (auto item : msg.nominal_touch_down) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: touch_down
  {
    if (msg.touch_down.size() == 0) {
      out << "touch_down: []";
    } else {
      out << "touch_down: [";
      size_t pending_items = msg.touch_down.size();
      for (auto item : msg.touch_down) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: swing_period
  {
    if (msg.swing_period.size() == 0) {
      out << "swing_period: []";
    } else {
      out << "swing_period: [";
      size_t pending_items = msg.swing_period.size();
      for (auto item : msg.swing_period) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: normal_force_max
  {
    if (msg.normal_force_max.size() == 0) {
      out << "normal_force_max: []";
    } else {
      out << "normal_force_max: [";
      size_t pending_items = msg.normal_force_max.size();
      for (auto item : msg.normal_force_max) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: normal_force_min
  {
    if (msg.normal_force_min.size() == 0) {
      out << "normal_force_min: []";
    } else {
      out << "normal_force_min: [";
      size_t pending_items = msg.normal_force_min.size();
      for (auto item : msg.normal_force_min) {
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
  const TrajectoryGenerator & msg,
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

  // member: com_pose
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "com_pose:\n";
    to_block_style_yaml(msg.com_pose, out, indentation + 2);
  }

  // member: com_vel
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "com_vel:\n";
    to_block_style_yaml(msg.com_vel, out, indentation + 2);
  }

  // member: com_acc
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "com_acc:\n";
    to_block_style_yaml(msg.com_acc, out, indentation + 2);
  }

  // member: joints_position
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.joints_position.size() == 0) {
      out << "joints_position: []\n";
    } else {
      out << "joints_position:\n";
      for (auto item : msg.joints_position) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: joints_velocity
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.joints_velocity.size() == 0) {
      out << "joints_velocity: []\n";
    } else {
      out << "joints_velocity:\n";
      for (auto item : msg.joints_velocity) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: joints_acceleration
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.joints_acceleration.size() == 0) {
      out << "joints_acceleration: []\n";
    } else {
      out << "joints_acceleration:\n";
      for (auto item : msg.joints_acceleration) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: joints_effort
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.joints_effort.size() == 0) {
      out << "joints_effort: []\n";
    } else {
      out << "joints_effort:\n";
      for (auto item : msg.joints_effort) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: kp
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.kp.size() == 0) {
      out << "kp: []\n";
    } else {
      out << "kp:\n";
      for (auto item : msg.kp) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: kd
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.kd.size() == 0) {
      out << "kd: []\n";
    } else {
      out << "kd:\n";
      for (auto item : msg.kd) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: wrench
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.wrench.size() == 0) {
      out << "wrench: []\n";
    } else {
      out << "wrench:\n";
      for (auto item : msg.wrench) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: stance_legs
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.stance_legs.size() == 0) {
      out << "stance_legs: []\n";
    } else {
      out << "stance_legs:\n";
      for (auto item : msg.stance_legs) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: nominal_touch_down
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.nominal_touch_down.size() == 0) {
      out << "nominal_touch_down: []\n";
    } else {
      out << "nominal_touch_down:\n";
      for (auto item : msg.nominal_touch_down) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: touch_down
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.touch_down.size() == 0) {
      out << "touch_down: []\n";
    } else {
      out << "touch_down:\n";
      for (auto item : msg.touch_down) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: swing_period
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.swing_period.size() == 0) {
      out << "swing_period: []\n";
    } else {
      out << "swing_period:\n";
      for (auto item : msg.swing_period) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: normal_force_max
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.normal_force_max.size() == 0) {
      out << "normal_force_max: []\n";
    } else {
      out << "normal_force_max:\n";
      for (auto item : msg.normal_force_max) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: normal_force_min
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.normal_force_min.size() == 0) {
      out << "normal_force_min: []\n";
    } else {
      out << "normal_force_min:\n";
      for (auto item : msg.normal_force_min) {
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

inline std::string to_yaml(const TrajectoryGenerator & msg, bool use_flow_style = false)
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
  const dls2_interfaces::msg::TrajectoryGenerator & msg,
  std::ostream & out, size_t indentation = 0)
{
  dls2_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use dls2_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const dls2_interfaces::msg::TrajectoryGenerator & msg)
{
  return dls2_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<dls2_interfaces::msg::TrajectoryGenerator>()
{
  return "dls2_interfaces::msg::TrajectoryGenerator";
}

template<>
inline const char * name<dls2_interfaces::msg::TrajectoryGenerator>()
{
  return "dls2_interfaces/msg/TrajectoryGenerator";
}

template<>
struct has_fixed_size<dls2_interfaces::msg::TrajectoryGenerator>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<dls2_interfaces::msg::TrajectoryGenerator>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<dls2_interfaces::msg::TrajectoryGenerator>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // DLS2_INTERFACES__MSG__DETAIL__TRAJECTORY_GENERATOR__TRAITS_HPP_
