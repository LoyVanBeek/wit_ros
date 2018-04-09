#!/usr/bin/env python
"""ROS node for the Wit.ai API"""

global APIKEY
APIKEY = None

import rospy
import requests
import json
from wit import Wit

from wit_ros.srv import Interpret, InterpretResponse, ListenAndInterpret, ListenAndInterpretResponse
from wit_ros.msg import Outcome, Entity

class WitRos(object):
    def __init__(self, api_key):
        self.wit = Wit(api_key)
        self.pub = rospy.Publisher('stt', Outcome, queue_size=1)

    def start(self):
        rospy.Service('wit/interpret', Interpret, self.interpret)
        # rospy.Service('wit/listen_interpret', ListenAndInterpret, self.listen_and_interpret)

    def parse_response(self, response, klass):
        rospy.logdebug("Data: '{0}'".format(json.dumps(response, indent=4, separators=(',', ': '))))
        ros_entities = []

        entities = response["outcomes"][0]["entities"]

        for entity_name, entity_properties in entities.iteritems():
            entity_properties = entity_properties[0]
            rospy.logdebug("Entity '{name}' has properties{prop}".format(name=entity_name, prop=entity_properties))

            entity = Entity(name=str(entity_name))
            if 'type' in entity_properties:
                entity.type = str(entity_properties["type"])
            if 'value' in entity_properties:
                entity.value = str(entity_properties["value"])
            if 'unit' in entity_properties:
                entity.unit = str(entity_properties["unit"])
            if 'suggested' in entity_properties:
                entity.suggested = str(entity_properties["suggested"])
            if 'confidence' in entity_properties:
                entity.confidence = float(entity_properties["confidence"])
            rospy.logdebug("Adding {ent}".format(ent=entity))
            ros_entities += [entity]

        outcome = Outcome(entities = ros_entities,
                          intent   = str(response.get("intent", "")),
                          text     = str(response["_text"]))

        response = klass(   msg_body    = str(response),
                            msg_id      = str(response["msg_id"]),
                            outcome     = outcome)
        self.pub.publish(outcome)

        return response

    def interpret(self, rosrequest):
        sentence = rosrequest.sentence
        rospy.logdebug("Interpreting '{0}'".format(sentence))
        wit_response = self.wit.message(sentence)
        rospy.logdebug("WitResponse: {0}".format(wit_response))
        #response = json.loads(wit_response)
        #rospy.logdebug("Response: {0}".format(response))

        return self.parse_response(wit_response, InterpretResponse)

    # TODO: wit.voice_query_auto used to take care of oudio recording, now it needs an audio file or encoded audio byte
    # def listen_and_interpret(self, rosrequest):
    #     rospy.logdebug("About to record audio")
    #     response = json.loads(self.wit.voice_query_auto(APIKEY))
    #     rospy.logdebug("Response: {0}".format(response))
    #     if not response:
    #         return None
    #
    #     return self.parse_response(response, ListenAndInterpretResponse)

if __name__ == "__main__":
    rospy.init_node("wit_ros", log_level=rospy.INFO)

    if rospy.has_param('~api_key'):
        APIKEY = rospy.get_param("~api_key")

        wr = WitRos(APIKEY)

        wr.start()

        rospy.spin()

    else:
        rospy.logerr("No API key set (via parameter server). Please set one. " +
            "API keys can be obtained via the http://www.wit.ai")
