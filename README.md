wit_ros
=======

Wrapper for the wit.ai natural language API

Be sure to create a file api.yaml in a param directory, like this:

  api_key: V.....Z
  
After rosmake-ing this package, you can run it with 
  roslaunch wit_ros start.launch

Then, run 

	$ rosservice call /wit/interpret "Hi there!"

This results in:

	msg_body: Hi there
	msg_id: 17783400-1075-44a4-a105-7f43754817e7
	outcome: 
  		confidence: 0.319000005722
  		intent: hello
  		entities: []

