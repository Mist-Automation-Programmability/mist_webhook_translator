
### WEB SERVER IMPORTS ###
from flask import Flask
from flask import json
from flask import request
### OTHER IMPORTS ###
import json
from libs import req
import os
import time
from datetime import datetime
###########################
### LOADING SETTINGS
from config import mist_conf
from config import slack_conf
from config import msteams_conf
from config import color_config
from config import message_levels

apitoken = mist_conf["apitoken"]
mist_host = mist_conf["mist_host"]
server_uri = mist_conf["server_uri"]
site_id_ignored = mist_conf["site_id_ignored"]

from libs.slack import Slack
slack = Slack(slack_conf)
from libs.msteams import Teams
teams = Teams(msteams_conf)
from libs.audit import audit
from libs.device_event import device_event
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
try:
    from config import port as server_port
except:
    server_port = 51361

###########################
### FUNCTIONS

def _title(topic, time):
    return "%s - %s" % (time, topic)

def _get_time(event):
    if "timestamp" in event:
        dt = datetime.fromtimestamp(event["timestamp"])
    else:
        dt = datetime.now()
    return "%s UTC" %(dt)

def new_event(topic, event):
    console.info("%s" %topic)

    message = []
    for key in event:
        console.info("%s: %s\r" %(key, event[key]))
        message.append("%s: %s" %(key, event[key]))

    if topic in color_config:
        color = color_config[topic]
    else:
        color = None

    if topic == "audits":
        level, text, actions = audit(topic, mist_host, mist_conf["approved_admins"], event)
    elif topic == "device-events":
        level, text, actions = device_event(topic, mist_host, message_levels, event)
    elif topic == "device-updowns":
        level, text, actions = device_event(topic, mist_host, message_levels, event)
    else:
        text = []
        level = "unknown"
        actions = []
        for mpart in message:
            text.append(mpart)        

    time = _get_time(event)
    if slack_conf["enabled"]: slack.send_manual_message(_title(topic, time), text, level, color, actions)
    if msteams_conf["enabled"]: teams.send_manual_message(topic, time, text, level, color, actions)
    print(event)
    print(topic)
    print(message)
    print("------")




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


