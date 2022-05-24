"""System modules"""
import sys
from datetime import datetime
import hmac
import hashlib
import os
from flask import Flask, request, render_template

import mwtt.src.mwtt as Mwtt
from mwtt.src.libs.logger import Console
"""App Settings"""
DEBUG = False
SERVER_PORT = 51361

try:
    from config import debug as DEBUG
except:
    DEBUG=False
finally:
    if not DEBUG:
        os.environ['FLASK_ENV'] = 'PRODUCTION'


try:
    from config import port as SERVER_PORT
except:
    pass

console = Console("main")
#######################################
#  FUNCTIONS


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
    console.notice(f"MWTT URI        : {SERVER_URI}")
    console.notice(f"Debug Mode      : {DEBUG}")


###########################
# ENTRY POINT
console.notice("Loading configuration ".center(80, "_"))
SERVER_URI = load_conf("server_uri")
console.notice("Configuration loaded".center(80, "_"))
display_conf()

app = Flask(__name__)


@app.route(SERVER_URI, methods=["POST"])
def postJsonHandler():
    return Mwtt.new_event("", request)
    
@app.route('/login', method="GET")
def getLogin():
    print("login")

if __name__ == '__main__':
    console.notice("Starting Server".center(80, "_"))
    app.run(debug=False, host='0.0.0.0', port=SERVER_PORT)
