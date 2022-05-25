import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRIPT_DIR)

"""System modules"""
from datetime import datetime
import hmac
import hashlib
from libs import slack as Slack
from libs import msteams as Teams
from libs.audit import audit
from libs.device_event import device_event
from libs.alarm import alarm
from libs.device_updown import device_updown
from libs.logger import Console
console = Console("mwtt")

#######################################
#  FUNCTIONS


def _get_time(event):
    if "timestamp" in event:
        dt = datetime.fromtimestamp(event["timestamp"])
    else:
        dt = datetime.now()
    return f"{dt} UTC"


def _process_event(topic, event, mist_conf, channels, slack_conf, msteams_conf):
    """Process new event"""
    console.info(f"Message topic: {topic}")

    if topic == "audits":
        data = audit(
            mist_conf.get("mist_host", None),
            mist_conf.get("approved_admins", []),
            channels.get("audit_channels", {}),
            event
        )
    elif topic == "device-events":
        data = device_event(
            mist_conf.get("mist_host", None),
            channels.get("event_channels", {}),
            event
        )
    elif topic == "device-updowns":
        data = device_updown(
            mist_conf.get("mist_host", None),
            channels.get("updown_channels", {}),
            event)
    elif topic == "alarms":
        data = alarm(
            mist_conf.get("mist_host", None),
            channels.get("alarm_channels", {}),
            event
        )
    else:
        data = {
            "text": "",
            "actions": [],
            "info": []}
        for key in event:
            data["info"].append(f"{key}: {event[key]}")

    # dt = _get_time(event)

    if slack_conf["enabled"]:
        Slack.send_manual_message(
            slack_conf,
            topic,
            data["title"],
            data["text"],
            data["info"],
            data["actions"],
            data["channel"]
        )
    if msteams_conf["enabled"]:
        Teams.send_manual_message(
            msteams_conf,
            topic,
            data["title"],
            data["text"],
            data["info"],
            data["actions"],
            data["channel"]
        )


def new_event(req, mist_conf, channels, slack_conf, msteams_conf):
    '''
    Start to process new webhook message
    request         flask request
    secret          str             webhook secret
    host            str             Mist Cloud host (api.mist.com, ...)
    approved_admins str             List of approved admins (used for audit logs)
    channels        obj             channels config:
                                        {
                                            event_channels: {},
                                            updown_channels: {},
                                            alarm_channels: {},
                                            audit_channels: {}
                                        }
    slack_conf      obj             slack configuration (enable: bool, default_url: str, url: {})
    msteams_conf    obj             MsTeams configuration (enable: bool, default_url: str, url: {})
    console         console
    '''
    start =  datetime.now()
    signature = req.headers['X-Mist-Signature'] if "X-Mist-Signature" in req.headers else None
    key = str.encode(mist_conf.get("mist_secret", None))
    message = req.data
    digester = hmac.new(key, message, hashlib.sha1).hexdigest()
    if signature != digester and mist_conf.get("secret", None):
        console.error("Webhook signature doesn't match")
        delta = datetime.now() - start
        console.info(f"Processing time {delta.seconds}.{delta.microseconds}s")
        return '', 401
    else:
        console.info("Processing new webhook message")
        content = req.get_json()
        console.debug(content)
        topic = content["topic"]
        events = content["events"]
        for event in events:
            _process_event(
                topic,
                event,
                mist_conf,
                channels,
                slack_conf,
                msteams_conf
            )
        delta = datetime.now() - start
        console.info(f"Processing time {delta.seconds}.{delta.microseconds}s")
        return '', 200
