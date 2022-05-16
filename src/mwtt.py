"""System modules"""
import sys
from datetime import datetime
import hmac
import hashlib
import os
from flask import Flask
from flask import request
from config import mist_conf
from config import slack_conf
from config import msteams_conf
from config import event_channels
from config import updown_channels
from config import alarm_channels
from config import audit_channels
from libs.slack import Slack
from libs.msteams import Teams
from libs.audit import audit
from libs.device_event import device_event
from libs.alarm import alarm
from libs.debug import Console
"""App Settings"""
SLACK = Slack(slack_conf)
TEAMS = Teams(msteams_conf)
DEBUG = False
LOG_LEVEL = 6
SERVER_PORT = 51361

try:
    from config import debug as DEBUG
except:
    DEBUG=False
finally:
    if not DEBUG:
        os.environ['FLASK_ENV'] = 'PRODUCTION'

try:
    from config import log_level as LOG_LEVEL
except:
    pass
finally:
    console = Console(LOG_LEVEL)

try:
    from config import port as SERVER_PORT
except:
    pass

#######################################
#  FUNCTIONS

def _get_time(event):
    if "timestamp" in event:
        dt = datetime.fromtimestamp(event["timestamp"])
    else:
        dt = datetime.now()
    return f"{0} UTC".format(dt)


def new_event(topic, event):
    """Process new event"""
    console.info(f"{0}".format(topic))

    message = []
    for key in event:
        console.info(f"{key}: {event[key]}\r")
        message.append(f"{key}: {event[key]}")

    if topic == "audits":
        data = audit(
            MIST_HOST, APPROVED_ADMINS, audit_channels, event)
    elif topic == "device-events":
        data = device_event(
            MIST_HOST, event_channels, event)
    elif topic == "device-updowns":
        data = device_event(
            MIST_HOST, updown_channels, event)
    elif topic == "alarms":
        data = alarm(
            MIST_HOST, alarm_channels, event)
    else:
        data = {
            "text": "",
            "actions": [],
            "info": []}
        for mpart in message:
            data["info"].append(mpart)

    # dt = _get_time(event)
    
    if slack_conf["enabled"]:
        SLACK.send_manual_message(
            topic, data["title"], data["text"], data["info"], data["actions"], data["channel"])
    if msteams_conf["enabled"]:
        TEAMS.send_manual_message(
            topic, data["title"], data["text"], data["info"], data["actions"], data["channel"])
    print(event)
    print(topic)
    print(message)
    print("------")

###########################
# CONF FUNCTIONS


def load_conf(value):
    """Process config"""
    print(f"Loading {value} ".ljust(79, "."), end="", flush=True)
    if value in mist_conf:
        print("\033[92m\u2714\033[0m")
        return mist_conf[value]
    else:
        print('\033[31m\u2716\033[0m')
        sys.exit(255)


def display_conf():
    """Display config"""
    print(f"Mist Hist       : {MIST_HOST}")
    print(f"API Token       : {APITOKEN[:6]}........{APITOKEN[len(APITOKEN)-6:]}")
    print(f"Webhook Secret  : {MIST_SECRET}")
    print(f"MWTT URI        : {SERVER_URI}")
    print(f"Ignored Sites   : {SITE_ID_IGNORED}")
    print(f"Approved Admins : {APPROVED_ADMINS}")
    print(f"Debug Mode      : {DEBUG}")


###########################
# ENTRY POINT
print("Loading configuration ".center(80, "_"))
APITOKEN = load_conf("apitoken")
MIST_HOST = load_conf("mist_host")
MIST_SECRET = load_conf("mist_secret")
SERVER_URI = load_conf("server_uri")
SITE_ID_IGNORED = load_conf("site_id_ignored")
APPROVED_ADMINS = load_conf("approved_admins")
print("Configuraiton loaded".center(80, "_"))
display_conf()

app = Flask(__name__)


@app.route(SERVER_URI, methods=["POST"])
def postJsonHandler():
    signature = request.headers['X-Mist-Signature'] if "X-Mist-Signature" in request.headers else None
    content = request.get_json()
    key = str.encode(MIST_SECRET)
    message = request.data
    digester = hmac.new(key, message, hashlib.sha1).hexdigest()
    if signature != digester and MIST_SECRET:
        return '', 401
    else:
        content = request.get_json()
        if DEBUG:
            print(content)
        topic = content["topic"]
        events = content["events"]
        for event in events:
            new_event(topic, event)
        return '', 200


if __name__ == '__main__':
    print("Starting Server".center(80, "_"))
    app.run(debug=False, host='0.0.0.0', port=SERVER_PORT)
