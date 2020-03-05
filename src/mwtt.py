
### WEB SERVER IMPORTS ###
from flask import Flask
from flask import json
from flask import request
### OTHER IMPORTS ###
import json
from libs import req
import os
import time

###########################
### LOADING SETTINGS
from config import mist_conf
from config import slack_conf

apitoken = mist_conf["apitoken"]
mist_cloud = mist_conf["mist_cloud"]
server_uri = mist_conf["server_uri"]
site_id_ignored = mist_conf["site_id_ignored"]

from libs.slack import Slack
slack = Slack(slack_conf)
###########################
### LOGGING SETTINGS
try:
    from config import log_level
except:
    log_level = 6
finally:
    from libs.debug import Console
    console = Console(log_level)


###########################
### VARS
server_port = 51361

###########################
### FUNCTIONS

def new_event(topic, event):
    console.info("%s" %topic)
    message = ""
    for key in event:
        console.info("%s: %s\r" %(key, event[key]))
        message += "%s: %s\r" %(key, event[key])
        if key == "type":
            topic += " - %s" %(event[key])
    slack.send_manual_message(topic, message)

###########################
### ENTRY POINT
app = Flask(__name__)
@app.route(server_uri, methods=["POST"])
def postJsonHandler():
    content = request.get_json()
    topic = content["topic"]
    events = content["events"]
    for event in events:   
        new_event(topic, event)
    return '', 200


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=server_port)


