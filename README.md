wit_ros
=======

Wrapper for the wit.ai natural language API

Installation
------------

	$ git clone https://github.com/LoyVanBeek/wit_ros.git
	$ cd wit_ros
	$ cmake .
	$ rosmake

Be sure to create a file api.yaml in a param directory, like this:

        $ cd param
        $ vim api.yaml #Use any editor to edit the API key
          api_key: V.....Z #Get your API key/access token from https://console.wit.ai/#/settings
  
After rosmake-ing this package, you can run it with 
  roslaunch wit_ros start.launch

Then, run 

	$ rosservice call /wit/interpret "hi there"

This results in:

	msg_body: hi there
	msg_id: 17783400-1075-44a4-a105-7f43754817e7
	outcome: 
  		confidence: 0.319000005722
  		intent: hello
  		entities: []


TODO
----
- Catkinize this package. I've never worked with catkin before, so I stuck with rosbuild for now. 
