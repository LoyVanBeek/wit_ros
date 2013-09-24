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
    if callable(httpresponse.json):
        data = httpresponse.json()
    else:
        data = httpresponse.json
        
    rospy.logdebug("Data: {0}".format(data))

    all_entities = []
    for name, entities in data["outcome"]["entities"].iteritems():
        if not isinstance(entities, list):
            entities = [entities]

        entities = [Entity(name  = str(name),
                           body  = str(e["body"]),
                           start = int(e["start"]),
                           end   = int(e["end"]),
                           value = str(e["value"])) for e in entities]

        all_entities += entities

    outcome = Outcome(          confidence  = float(data["outcome"]["confidence"]),
                                entities    = all_entities,
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