#!/usr/bin/env python
"""ROS node for the Wit.ai API"""

import roslib
roslib.load_manifest('wit_ros')

global APIKEY
APIKEY = None

import rospy
import requests

from wit_ros.srv import Interpret, InterpretResponse
from wit_ros.msg import Outcome, Entity

def interpret(rosrequest):
    rospy.logdebug("Interpreting {0}".format(rosrequest.sentence))
    httpresponse = requests.get('https://api.wit.ai/message?q={sentence}'.format(sentence=rosrequest.sentence), 
        headers={"Authorization":"Bearer {key}".format(key=APIKEY)})
    data = httpresponse.json()
    rospy.logdebug("Data: {0}".format(data))

    entities = []
    for name, json in data["outcome"]["entities"].iteritems():
        entity = Entity(name    = str(name),
                        body    = str(json["body"]),
                        start   = int(json["start"]),
                        end     = int(json["end"]),
                        value   = str(json["value"]))
        entities += [entity]

    outcome = Outcome(          confidence  = float(data["outcome"]["confidence"]), 
                                entities    = entities,
                                intent      = str(data["outcome"]["intent"]))

    response = InterpretResponse(   msg_body    = str(data["msg_body"]),
                                    msg_id      = str(data["msg_id"]),
                                    outcome     = outcome)
    return response

if __name__ == "__main__":
    rospy.init_node("wit_ros")

    if rospy.has_param('~api_key'):
        APIKEY = rospy.get_param("~api_key")

        rospy.Service('wit/interpret', Interpret, interpret)

        rospy.spin()

    else:
        rospy.logerr("No API key set (via parameter server). Please set one. " +
            "API keys can be obtained via the http://www.wit.ai")