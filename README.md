### TODO:
- [ ] Subscribe to an audio stream topic and analyze

wit_ros
=======

Wrapper for the [wit.ai](http://www.wit.ai) natural language API

Installation
------------

        $ sudo pip install wit
        $ cd catkin_ws/src
        $ git clone https://github.com/LoyVanBeek/wit_ros.git
        $ cd catkin_ws
        $ catkin_make

Be sure to create a file api.yaml in a param directory, like this:

        $ roscd wit_ros/param
        $ vim api.yaml #Use any editor to edit the API key
          api_key: V.....Z #Get your API key/access token from https://console.wit.ai/#/settings
  
After rosmake-ing this package, you can run it with 

       $ roslaunch wit_ros start.launch

Then, run 

        $ rosservice call /wit/interpret "sentence: 'Clean up the table in the living room'"

Which outputs: 

```yaml
msg_body: {u'outcomes': [{u'entities': {u'item': [{u'type': u'value', u'value': u'the table'}], u'location': [{u'suggested': True, u'type': u'value', u'value': u'living room'}]}, u'confidence': 0.998, u'intent': u'cleanup', u'_text': u'Clean up the table in the living room'}], u'msg_id': u'fcdd89ed-2984-464e-89e6-fce78060e54e', u'_text': u'Clean up the table in the living room'}
msg_id: fcdd89ed-2984-464e-89e6-fce78060e54e
outcome: 
  confidence: 0.998000025749
  intent: cleanup
  entities: 
    - 
      name: item
      type: value
      value: the table
      unit: ''
      suggested: ''
    - 
      name: location
      type: value
      value: living room
      unit: ''
      suggested: True
```

Or, run 

        $ rosservice call /wit/listen_interpret

And just say your command!
