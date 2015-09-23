### TODO:
- [ ] Subscribe to an audio stream topic and analyze 

wit_ros
=======

Wrapper for the wit.ai natural language API

Installation
------------

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

        $ rosservice call /wit/interpret "hi there"

This results in:

	msg_body: hi there
	msg_id: 17783400-1075-44a4-a105-7f43754817e7
	outcome: 
  		confidence: 0.319000005722
  		intent: hello
  		entities: []
