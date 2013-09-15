#!/usr/bin/env python
"""ROS node for the Wit.ai API"""

import roslib
roslib.load_manifest('wit_ros')

from wit_ros.srv import Interpret, InterpretResponse
