#!/usr/bin/env python
"""ROS node for the Wit.ai API"""

global APIKEY
APIKEY = None

import rospy
import requests
import json
import wit

from wit_ros.srv import Interpret, InterpretResponse, ListenAndInterpret, ListenAndInterpretResponse
from wit_ros.msg import Outcome, Entity

def parse_response(response, klass):
    rospy.logdebug("Data: {0}".format(json.dumps(response, indent=4, separators=(',', ': '))))
    ros_entities = []

    entities = response["outcomes"][0]["entities"]

    for entity_name, entity_properties in entities.iteritems():
        entity_properties = entity_properties[0]
        entity = Entity(name=str(entity_name))
        if 'type' in entity_properties:
            entity.type = str(entity_properties["type"])
        if 'value' in entity_properties:
            entity.value = str(entity_properties["value"])
        if 'unit' in entity_properties:
            entity.unit = str(entity_properties["unit"])
        if 'suggested' in entity_properties:
            entity.suggested = str(entity_properties["suggested"])
        ros_entities += [entity]

    outcome = Outcome(          confidence  = float(response["outcomes"][0]["confidence"]),
                                entities    = ros_entities,
                                intent      = str(response["outcomes"][0]["intent"]))

    response = klass(   msg_body    = str(response),
                                    msg_id      = str(response["msg_id"]),
                                    outcome     = outcome)
    pub.publish(outcome)

    return response

def interpret(rosrequest):
    sentence = rosrequest.sentence
    rospy.logdebug("Interpreting {0}".format(sentence))
    response = json.loads(wit.text_query(sentence, APIKEY))
    rospy.logdebug("Response: {0}".format(response))

    return parse_response(response, InterpretResponse)

def listen_and_interpret(rosrequest):
    rospy.logdebug("About to record audio")
    response = json.loads(wit.voice_query_auto(APIKEY))
    rospy.logdebug("Response: {0}".format(response))
    if not response:
        return None

    return parse_response(response, ListenAndInterpretResponse)

def shutdown():
  wit.close()

if __name__ == "__main__":
    rospy.init_node("wit_ros", log_level=rospy.INFO)
    rospy.on_shutdown(shutdown)
    pub = rospy.Publisher('stt', Outcome, queue_size=1)

    wit.init()

    if rospy.has_param('~api_key'):
        APIKEY = rospy.get_param("~api_key")

        rospy.Service('wit/interpret', Interpret, interpret)
        rospy.Service('wit/listen_interpret', ListenAndInterpret, listen_and_interpret)

        rospy.spin()

    else:
        rospy.logerr("No API key set (via parameter server). Please set one. " +
            "API keys can be obtained via the http://www.wit.ai")
