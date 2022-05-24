"""System modules"""
import os
import sys
from flask import Flask
from flask import request
from config import mist_conf
from config import slack_conf
from config import msteams_conf
from config import event_channels
from config import updown_channels
from config import alarm_channels
from config import audit_channels
###########################
# APP SETTINGS
DEBUG = False
LOG_LEVEL = "INFO"
SERVER_PORT = 51361

try:
    import config
    if hasattr(config, 'debug'):
        DEBUG = config.debug
    if hasattr(config, 'log_level'):
        print(config.log_level)
        LOG_LEVEL = config.log_level
    if hasattr(config, 'port'):
        SERVER_PORT = config.port
except:
    pass
finally:
    os.environ["LOG_LEVEL"]= LOG_LEVEL
    if not DEBUG:
        os.environ['FLASK_ENV'] = 'PRODUCTION'
    import mwtt
    from libs.logger import Console
    console = Console("main")
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
    print(
        f"API Token       : {APITOKEN[:6]}........{APITOKEN[len(APITOKEN)-6:]}")
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
    console.info(" New message reveived ".center(60, "-"))
    res= mwtt.new_event(
        request,
        mist_conf,
        {
            "event_channels": event_channels,
            "updown_channels": updown_channels,
            "alarm_channels": alarm_channels,
            "audit_channels": audit_channels
        },
        slack_conf,
        msteams_conf
    )
    return res
    # mwtt.new_event(topic, event)


if __name__ == '__main__':
    print(f"Starting Server: 0.0.0.0:{SERVER_PORT}".center(80, "_"))
    app.run(debug=False, host='0.0.0.0', port=SERVER_PORT)
