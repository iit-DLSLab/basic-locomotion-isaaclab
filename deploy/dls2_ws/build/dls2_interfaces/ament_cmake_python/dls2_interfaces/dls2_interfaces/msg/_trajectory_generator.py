# generated from rosidl_generator_py/resource/_idl.py.em
# with input from dls2_interfaces:msg/TrajectoryGenerator.idl
# generated code does not contain a copyright notice


# Import statements for member types

# Member 'joints_position'
# Member 'joints_velocity'
# Member 'joints_acceleration'
# Member 'joints_effort'
# Member 'kp'
# Member 'kd'
# Member 'nominal_touch_down'
# Member 'touch_down'
# Member 'swing_period'
# Member 'normal_force_max'
# Member 'normal_force_min'
import array  # noqa: E402, I100

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

# Member 'wrench'
import numpy  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_TrajectoryGenerator(type):
    """Metaclass of message 'TrajectoryGenerator'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('dls2_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'dls2_interfaces.msg.TrajectoryGenerator')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__trajectory_generator
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__trajectory_generator
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__trajectory_generator
            cls._TYPE_SUPPORT = module.type_support_msg__msg__trajectory_generator
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__trajectory_generator

            from dls2_interfaces.msg import Pose
            if Pose.__class__._TYPE_SUPPORT is None:
                Pose.__class__.__import_type_support__()

            from dls2_interfaces.msg import Screw
            if Screw.__class__._TYPE_SUPPORT is None:
                Screw.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class TrajectoryGenerator(metaclass=Metaclass_TrajectoryGenerator):
    """Message class 'TrajectoryGenerator'."""

    __slots__ = [
        '_frame_id',
        '_sequence_id',
        '_timestamp',
        '_com_pose',
        '_com_vel',
        '_com_acc',
        '_joints_position',
        '_joints_velocity',
        '_joints_acceleration',
        '_joints_effort',
        '_kp',
        '_kd',
        '_wrench',
        '_stance_legs',
        '_nominal_touch_down',
        '_touch_down',
        '_swing_period',
        '_normal_force_max',
        '_normal_force_min',
    ]

    _fields_and_field_types = {
        'frame_id': 'string',
        'sequence_id': 'uint32',
        'timestamp': 'double',
        'com_pose': 'dls2_interfaces/Pose',
        'com_vel': 'dls2_interfaces/Screw',
        'com_acc': 'dls2_interfaces/Screw',
        'joints_position': 'sequence<double>',
        'joints_velocity': 'sequence<double>',
        'joints_acceleration': 'sequence<double>',
        'joints_effort': 'sequence<double>',
        'kp': 'sequence<double>',
        'kd': 'sequence<double>',
        'wrench': 'double[6]',
        'stance_legs': 'sequence<boolean>',
        'nominal_touch_down': 'sequence<double>',
        'touch_down': 'sequence<double>',
        'swing_period': 'sequence<double>',
        'normal_force_max': 'sequence<double>',
        'normal_force_min': 'sequence<double>',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['dls2_interfaces', 'msg'], 'Pose'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['dls2_interfaces', 'msg'], 'Screw'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['dls2_interfaces', 'msg'], 'Screw'),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('double')),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('double')),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('double')),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('double')),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('double')),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('double')),  # noqa: E501
        rosidl_parser.definition.Array(rosidl_parser.definition.BasicType('double'), 6),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('boolean')),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('double')),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('double')),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('double')),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('double')),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('double')),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.frame_id = kwargs.get('frame_id', str())
        self.sequence_id = kwargs.get('sequence_id', int())
        self.timestamp = kwargs.get('timestamp', float())
        from dls2_interfaces.msg import Pose
        self.com_pose = kwargs.get('com_pose', Pose())
        from dls2_interfaces.msg import Screw
        self.com_vel = kwargs.get('com_vel', Screw())
        from dls2_interfaces.msg import Screw
        self.com_acc = kwargs.get('com_acc', Screw())
        self.joints_position = array.array('d', kwargs.get('joints_position', []))
        self.joints_velocity = array.array('d', kwargs.get('joints_velocity', []))
        self.joints_acceleration = array.array('d', kwargs.get('joints_acceleration', []))
        self.joints_effort = array.array('d', kwargs.get('joints_effort', []))
        self.kp = array.array('d', kwargs.get('kp', []))
        self.kd = array.array('d', kwargs.get('kd', []))
        if 'wrench' not in kwargs:
            self.wrench = numpy.zeros(6, dtype=numpy.float64)
        else:
            self.wrench = numpy.array(kwargs.get('wrench'), dtype=numpy.float64)
            assert self.wrench.shape == (6, )
        self.stance_legs = kwargs.get('stance_legs', [])
        self.nominal_touch_down = array.array('d', kwargs.get('nominal_touch_down', []))
        self.touch_down = array.array('d', kwargs.get('touch_down', []))
        self.swing_period = array.array('d', kwargs.get('swing_period', []))
        self.normal_force_max = array.array('d', kwargs.get('normal_force_max', []))
        self.normal_force_min = array.array('d', kwargs.get('normal_force_min', []))

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.frame_id != other.frame_id:
            return False
        if self.sequence_id != other.sequence_id:
            return False
        if self.timestamp != other.timestamp:
            return False
        if self.com_pose != other.com_pose:
            return False
        if self.com_vel != other.com_vel:
            return False
        if self.com_acc != other.com_acc:
            return False
        if self.joints_position != other.joints_position:
            return False
        if self.joints_velocity != other.joints_velocity:
            return False
        if self.joints_acceleration != other.joints_acceleration:
            return False
        if self.joints_effort != other.joints_effort:
            return False
        if self.kp != other.kp:
            return False
        if self.kd != other.kd:
            return False
        if all(self.wrench != other.wrench):
            return False
        if self.stance_legs != other.stance_legs:
            return False
        if self.nominal_touch_down != other.nominal_touch_down:
            return False
        if self.touch_down != other.touch_down:
            return False
        if self.swing_period != other.swing_period:
            return False
        if self.normal_force_max != other.normal_force_max:
            return False
        if self.normal_force_min != other.normal_force_min:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def frame_id(self):
        """Message field 'frame_id'."""
        return self._frame_id

    @frame_id.setter
    def frame_id(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'frame_id' field must be of type 'str'"
        self._frame_id = value

    @builtins.property
    def sequence_id(self):
        """Message field 'sequence_id'."""
        return self._sequence_id

    @sequence_id.setter
    def sequence_id(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'sequence_id' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'sequence_id' field must be an unsigned integer in [0, 4294967295]"
        self._sequence_id = value

    @builtins.property
    def timestamp(self):
        """Message field 'timestamp'."""
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'timestamp' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'timestamp' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._timestamp = value

    @builtins.property
    def com_pose(self):
        """Message field 'com_pose'."""
        return self._com_pose

    @com_pose.setter
    def com_pose(self, value):
        if __debug__:
            from dls2_interfaces.msg import Pose
            assert \
                isinstance(value, Pose), \
                "The 'com_pose' field must be a sub message of type 'Pose'"
        self._com_pose = value

    @builtins.property
    def com_vel(self):
        """Message field 'com_vel'."""
        return self._com_vel

    @com_vel.setter
    def com_vel(self, value):
        if __debug__:
            from dls2_interfaces.msg import Screw
            assert \
                isinstance(value, Screw), \
                "The 'com_vel' field must be a sub message of type 'Screw'"
        self._com_vel = value

    @builtins.property
    def com_acc(self):
        """Message field 'com_acc'."""
        return self._com_acc

    @com_acc.setter
    def com_acc(self, value):
        if __debug__:
            from dls2_interfaces.msg import Screw
            assert \
                isinstance(value, Screw), \
                "The 'com_acc' field must be a sub message of type 'Screw'"
        self._com_acc = value

    @builtins.property
    def joints_position(self):
        """Message field 'joints_position'."""
        return self._joints_position

    @joints_position.setter
    def joints_position(self, value):
        if isinstance(value, array.array):
            assert value.typecode == 'd', \
                "The 'joints_position' array.array() must have the type code of 'd'"
            self._joints_position = value
            return
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, float) for v in value) and
                 all(not (val < -1.7976931348623157e+308 or val > 1.7976931348623157e+308) or math.isinf(val) for val in value)), \
                "The 'joints_position' field must be a set or sequence and each value of type 'float' and each double in [-179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000, 179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000]"
        self._joints_position = array.array('d', value)

    @builtins.property
    def joints_velocity(self):
        """Message field 'joints_velocity'."""
        return self._joints_velocity

    @joints_velocity.setter
    def joints_velocity(self, value):
        if isinstance(value, array.array):
            assert value.typecode == 'd', \
                "The 'joints_velocity' array.array() must have the type code of 'd'"
            self._joints_velocity = value
            return
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, float) for v in value) and
                 all(not (val < -1.7976931348623157e+308 or val > 1.7976931348623157e+308) or math.isinf(val) for val in value)), \
                "The 'joints_velocity' field must be a set or sequence and each value of type 'float' and each double in [-179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000, 179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000]"
        self._joints_velocity = array.array('d', value)

    @builtins.property
    def joints_acceleration(self):
        """Message field 'joints_acceleration'."""
        return self._joints_acceleration

    @joints_acceleration.setter
    def joints_acceleration(self, value):
        if isinstance(value, array.array):
            assert value.typecode == 'd', \
                "The 'joints_acceleration' array.array() must have the type code of 'd'"
            self._joints_acceleration = value
            return
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, float) for v in value) and
                 all(not (val < -1.7976931348623157e+308 or val > 1.7976931348623157e+308) or math.isinf(val) for val in value)), \
                "The 'joints_acceleration' field must be a set or sequence and each value of type 'float' and each double in [-179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000, 179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000]"
        self._joints_acceleration = array.array('d', value)

    @builtins.property
    def joints_effort(self):
        """Message field 'joints_effort'."""
        return self._joints_effort

    @joints_effort.setter
    def joints_effort(self, value):
        if isinstance(value, array.array):
            assert value.typecode == 'd', \
                "The 'joints_effort' array.array() must have the type code of 'd'"
            self._joints_effort = value
            return
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, float) for v in value) and
                 all(not (val < -1.7976931348623157e+308 or val > 1.7976931348623157e+308) or math.isinf(val) for val in value)), \
                "The 'joints_effort' field must be a set or sequence and each value of type 'float' and each double in [-179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000, 179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000]"
        self._joints_effort = array.array('d', value)

    @builtins.property
    def kp(self):
        """Message field 'kp'."""
        return self._kp

    @kp.setter
    def kp(self, value):
        if isinstance(value, array.array):
            assert value.typecode == 'd', \
                "The 'kp' array.array() must have the type code of 'd'"
            self._kp = value
            return
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, float) for v in value) and
                 all(not (val < -1.7976931348623157e+308 or val > 1.7976931348623157e+308) or math.isinf(val) for val in value)), \
                "The 'kp' field must be a set or sequence and each value of type 'float' and each double in [-179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000, 179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000]"
        self._kp = array.array('d', value)

    @builtins.property
    def kd(self):
        """Message field 'kd'."""
        return self._kd

    @kd.setter
    def kd(self, value):
        if isinstance(value, array.array):
            assert value.typecode == 'd', \
                "The 'kd' array.array() must have the type code of 'd'"
            self._kd = value
            return
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, float) for v in value) and
                 all(not (val < -1.7976931348623157e+308 or val > 1.7976931348623157e+308) or math.isinf(val) for val in value)), \
                "The 'kd' field must be a set or sequence and each value of type 'float' and each double in [-179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000, 179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000]"
        self._kd = array.array('d', value)

    @builtins.property
    def wrench(self):
        """Message field 'wrench'."""
        return self._wrench

    @wrench.setter
    def wrench(self, value):
        if isinstance(value, numpy.ndarray):
            assert value.dtype == numpy.float64, \
                "The 'wrench' numpy.ndarray() must have the dtype of 'numpy.float64'"
            assert value.size == 6, \
                "The 'wrench' numpy.ndarray() must have a size of 6"
            self._wrench = value
            return
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 len(value) == 6 and
                 all(isinstance(v, float) for v in value) and
                 all(not (val < -1.7976931348623157e+308 or val > 1.7976931348623157e+308) or math.isinf(val) for val in value)), \
                "The 'wrench' field must be a set or sequence with length 6 and each value of type 'float' and each double in [-179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000, 179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000]"
        self._wrench = numpy.array(value, dtype=numpy.float64)

    @builtins.property
    def stance_legs(self):
        """Message field 'stance_legs'."""
        return self._stance_legs

    @stance_legs.setter
    def stance_legs(self, value):
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, bool) for v in value) and
                 True), \
                "The 'stance_legs' field must be a set or sequence and each value of type 'bool'"
        self._stance_legs = value

    @builtins.property
    def nominal_touch_down(self):
        """Message field 'nominal_touch_down'."""
        return self._nominal_touch_down

    @nominal_touch_down.setter
    def nominal_touch_down(self, value):
        if isinstance(value, array.array):
            assert value.typecode == 'd', \
                "The 'nominal_touch_down' array.array() must have the type code of 'd'"
            self._nominal_touch_down = value
            return
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, float) for v in value) and
                 all(not (val < -1.7976931348623157e+308 or val > 1.7976931348623157e+308) or math.isinf(val) for val in value)), \
                "The 'nominal_touch_down' field must be a set or sequence and each value of type 'float' and each double in [-179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000, 179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000]"
        self._nominal_touch_down = array.array('d', value)

    @builtins.property
    def touch_down(self):
        """Message field 'touch_down'."""
        return self._touch_down

    @touch_down.setter
    def touch_down(self, value):
        if isinstance(value, array.array):
            assert value.typecode == 'd', \
                "The 'touch_down' array.array() must have the type code of 'd'"
            self._touch_down = value
            return
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, float) for v in value) and
                 all(not (val < -1.7976931348623157e+308 or val > 1.7976931348623157e+308) or math.isinf(val) for val in value)), \
                "The 'touch_down' field must be a set or sequence and each value of type 'float' and each double in [-179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000, 179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000]"
        self._touch_down = array.array('d', value)

    @builtins.property
    def swing_period(self):
        """Message field 'swing_period'."""
        return self._swing_period

    @swing_period.setter
    def swing_period(self, value):
        if isinstance(value, array.array):
            assert value.typecode == 'd', \
                "The 'swing_period' array.array() must have the type code of 'd'"
            self._swing_period = value
            return
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, float) for v in value) and
                 all(not (val < -1.7976931348623157e+308 or val > 1.7976931348623157e+308) or math.isinf(val) for val in value)), \
                "The 'swing_period' field must be a set or sequence and each value of type 'float' and each double in [-179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000, 179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000]"
        self._swing_period = array.array('d', value)

    @builtins.property
    def normal_force_max(self):
        """Message field 'normal_force_max'."""
        return self._normal_force_max

    @normal_force_max.setter
    def normal_force_max(self, value):
        if isinstance(value, array.array):
            assert value.typecode == 'd', \
                "The 'normal_force_max' array.array() must have the type code of 'd'"
            self._normal_force_max = value
            return
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, float) for v in value) and
                 all(not (val < -1.7976931348623157e+308 or val > 1.7976931348623157e+308) or math.isinf(val) for val in value)), \
                "The 'normal_force_max' field must be a set or sequence and each value of type 'float' and each double in [-179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000, 179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000]"
        self._normal_force_max = array.array('d', value)

    @builtins.property
    def normal_force_min(self):
        """Message field 'normal_force_min'."""
        return self._normal_force_min

    @normal_force_min.setter
    def normal_force_min(self, value):
        if isinstance(value, array.array):
            assert value.typecode == 'd', \
                "The 'normal_force_min' array.array() must have the type code of 'd'"
            self._normal_force_min = value
            return
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, float) for v in value) and
                 all(not (val < -1.7976931348623157e+308 or val > 1.7976931348623157e+308) or math.isinf(val) for val in value)), \
                "The 'normal_force_min' field must be a set or sequence and each value of type 'float' and each double in [-179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000, 179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000]"
        self._normal_force_min = array.array('d', value)
