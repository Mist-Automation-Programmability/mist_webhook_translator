
### WEB SERVER IMPORTS ###
from flask import Flask
from flask import json
from flask import request
### OTHER IMPORTS ###
import json
from libs import req
import os
import time
from datetime import datetime, timedelta
import hmac, hashlib
###########################
### LOADING SETTINGS
from config import mist_conf
from config import slack_conf
from config import msteams_conf
from config import color_config
from config import message_levels


from libs.slack import Slack
slack = Slack(slack_conf)
from libs.msteams import Teams
teams = Teams(msteams_conf)
from libs.audit import audit
from libs.device_event import device_event
from libs.alarm import alarm
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
    return "{0} - {1}".format(time, topic)

def _get_time(event):
    if "timestamp" in event:
        dt = datetime.fromtimestamp(event["timestamp"])
    else:
        dt = datetime.now()
    return "{0} UTC".format(dt)

def new_event(topic, event):
    console.info("{0}".format(topic))

    message = []
    for key in event:
        console.info("%s: %s\r" %(key, event[key]))
        message.append("%s: %s" %(key, event[key]))

    if topic in color_config:
        color = color_config[topic]
    else:
        color = None

    if topic == "audits":
        level, text, actions = audit(topic, mist_host, approved_admins, event)
    elif topic == "device-events":
        level, text, actions = device_event(topic, mist_host, message_levels, event)
    elif topic == "device-updowns":
        level, text, actions = device_event(topic, mist_host, message_levels, event)
    elif topic == "alarms":
        level, text, actions = alarm(topic, mist_host, message_levels, event)
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
### CONF FUNCTIONS

def load_conf(value):
    print("Loading {0} ".format(value).ljust(79, "."), end="", flush=True)
    if value in mist_conf:
        print("\033[92m\u2714\033[0m")
        return mist_conf[value]
    else:
        print('\033[31m\u2716\033[0m')
        exit(255)

def display_conf():
    print("Mist Hist: {0}".format(mist_host))
    print("API Token: {0}........{1}".format(apitoken[:6], apitoken[len(apitoken)-6:]))
    print("Webhook Secret: {0}".format(mist_secret))
    print("MWTT URI: {0}".format(server_uri))
    print("Ignored Sites: {0}".format(site_id_ignored))
    print("Approved Admins: {0}".format(approved_admins))


###########################
### ENTRY POINT
print("Loading configuration ".center(80,"_")) 
apitoken  = load_conf("apitoken")
mist_host= load_conf("mist_host")
mist_secret= load_conf("mist_secret")
server_uri = load_conf("server_uri")
site_id_ignored= load_conf("site_id_ignored")
approved_admins= load_conf("approved_admins")
print("Configuraiton loaded".center(80, "_"))
display_conf()

app = Flask(__name__)
@app.route(server_uri, methods=["POST"])
def postJsonHandler():
    signature = request.headers['X-Mist-Signature'] if "X-Mist-Signature" in request.headers else None
    content = request.get_json()
    key = str.encode(mist_secret)
    message = request.data
    digester = hmac.new(key, message, hashlib.sha1).hexdigest()
    if signature == digester or mist_secret == None:
            
        content = request.get_json()
        topic = content["topic"]
        events = content["events"]
        for event in events:   
            new_event(topic, event)
        return '', 200
    else: 
        return '', 401


if __name__ == '__main__':
    print("Starting Server".center(80, "_"))
    app.run(debug=False, host='0.0.0.0', port=server_port)


