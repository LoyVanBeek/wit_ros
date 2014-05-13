#!/usr/bin/env python
"""ROS node for the Wit.ai API"""

import roslib
roslib.load_manifest('wit_ros')

global APIKEY
APIKEY = None

import rospy
import requests
import json

try:
    from sh import rec
except ImportError:
    print "Please install the 'rec' utility with 'sudo apt-get install sox' "

from wit_ros.srv import Interpret, InterpretResponse, ListenAndInterpret, ListenAndInterpretResponse
from wit_ros.msg import Outcome, Entity

def parse_response(httpresponse, klass):
    if callable(httpresponse.json):
        data = httpresponse.json()
    else:
        data = httpresponse.json
        
    rospy.logdebug("Data: {0}".format(json.dumps(data, indent=4, separators=(',', ': '))))

    ros_entities = []

    for entity_name, entity_properties in data["outcome"]["entities"].iteritems():   
        entity = Entity(name=str(entity_name))
        if 'body' in entity_properties: 
            entity.body = str(entity_properties["body"])
        if 'start' in entity_properties: 
            entity.start = int(entity_properties["start"]) 
        if 'end' in entity_properties: 
            entity.end = int(entity_properties["end"]) 
        if 'value' in entity_properties: 
            entity.value = str(entity_properties["value"])
        ros_entities += [entity]

    outcome = Outcome(          confidence  = float(data["outcome"]["confidence"]),
                                entities    = ros_entities,
                                intent      = str(data["outcome"]["intent"]))

    response = klass(   msg_body    = str(data["msg_body"]),
                                    msg_id      = str(data["msg_id"]),
                                    outcome     = outcome)
    return response

def interpret(rosrequest):
    rospy.logdebug("Interpreting {0}".format(rosrequest.sentence))
    httpresponse = requests.get('http://api.wit.ai/message?v=20140401&q={sentence}'.format(sentence=rosrequest.sentence), 
        headers={"Authorization":"Bearer {key}".format(key=APIKEY)})
    rospy.logdebug(httpresponse)

    return parse_response(httpresponse, InterpretResponse)

def listen_and_interpret(rosrequest):
    rospy.loginfo("Recording audio sample")
    rec("/tmp/sample.wav", "silence", "-l", "1", "5", "20%", "1", "0:00:02", "15%") #Record an audio fragment
    #import ipdb; ipdb.set_trace()
    sample = open('/tmp/sample.wav', 'rb')

    rospy.loginfo("Done, interpreting audio sample")
    httpresponse = requests.post('https://api.wit.ai/speech', 
        headers={"Authorization":"Bearer {key}".format(key=APIKEY),
                 "Content-type":"audio/wav"}, data=sample)
    rospy.logdebug(httpresponse)
    if httpresponse.status_code != 200:
        return None

    return parse_response(httpresponse, ListenAndInterpretResponse)

if __name__ == "__main__":
    rospy.init_node("wit_ros", log_level=rospy.INFO)

    if rospy.has_param('~api_key'):
        APIKEY = rospy.get_param("~api_key")

        rospy.Service('wit/interpret', Interpret, interpret)
        rospy.Service('wit/listen_interpret', ListenAndInterpret, listen_and_interpret)

        rospy.spin()

    else:
        rospy.logerr("No API key set (via parameter server). Please set one. " +
            "API keys can be obtained via the http://www.wit.ai")
