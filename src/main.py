from mwtt import Console
from mwtt.src import mwtt as Mwtt
from routes import api_login, api_orgs, api_webhooks, collector
from pymongo import MongoClient
import html
from datetime import date, datetime, timedelta, timezone
from flask_session import Session
from flask import Flask, session, request, render_template, redirect, g
import functools
import os
from dotenv import load_dotenv


def getenv_bool(variable):
    if os.getenv(variable, False) in [ 1, True, "true", "TRUE", "True" ]:
        return True
    return False


load_dotenv()
DEBUG = getenv_bool('FLASK_DEBUG')
if DEBUG:
    os.environ['FLASK_ENV'] = 'PRODUCTION'
    os.environ["LOG_LEVEL"] = "DEBUG"
else:
    os.environ["LOG_LEVEL"] = "INFO"

FLASK_SECRET = os.getenv('FLASK_SECRET')
FLASK_PORT = os.getenv('FLASK_PORT', 51360)
MONGO_USER = os.getenv('MONGO_USER')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
MONGO_HOST = os.getenv('MONGO_HOST')
MONGO_PORT = os.getenv('MONGO_PORT', 27017)
MONGO_DB = os.getenv('MONGO_DB', 'translator')
WH_HOST = os.getenv('WH_HOST')
WH_HTTPS = getenv_bool('WH_HTTPS')
WH_PORT = os.getenv('WH_PORT', 51360)
WH_PREFIX = os.getenv('WH_PREFIX', 'webhooks')
ABOUT_TOKEN = os.getenv('ABOUT_TOKEN', 'secret_token')
if WH_HTTPS:
    WH_COLLECTOR = f"https://{WH_HOST}:{WH_PORT}/{WH_PREFIX}"
else:
    WH_COLLECTOR = f"http://{WH_HOST}:{WH_PORT}/{WH_PREFIX}"

"""System modules"""
#from flask_pymongo import PyMongo


console = Console("main")
#######################################
#  FUNCTIONS


def display_conf():
    """Display config"""
    console.info(f"Debug Mode        : {DEBUG}")
    console.info(f"Server Port       : {FLASK_PORT}")
    console.info(f"MongoDb Server    : {MONGO_HOST}")
    console.info(f"MongoDb Port      : {MONGO_PORT}")
    console.info(f"MongoDb User      : {MONGO_USER}")
    console.info(f"MongoDb Database  : {MONGO_DB}")
    console.info(f"Webhooks collector: {WH_COLLECTOR}/<org_id>")
    console.info(f"About Token       : {ABOUT_TOKEN}")


###########################
# ENTRY POINT

#######
# FLASK
console.info("Loading configuration ".center(40, "_"))
console.info("Configuration loaded".center(40, "_"))
display_conf()

app = Flask(__name__)
#######
# MONGO
mongodb_client = MongoClient(
    f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/?authSource=admin")
db = mongodb_client[MONGO_DB]

app.secret_key = FLASK_SECRET
app.config['SESSION_TYPE'] = 'mongodb'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_MONGODB'] = mongodb_client
app.config['SESSION_MONGODB_DB'] = "flask-session"
app.config['SESSION_MONGODB_COLLECT'] = "translator"
server_session = Session()
server_session.init_app(app)

session_db = mongodb_client["flask-session"]


def clean_session_db():
    for session in session_db.translator.find({}):
        expired = session["expiration"].replace(
            tzinfo=timezone.utc).timestamp() < datetime.today().timestamp()
        print(expired)
        if expired:
            session_db.translator.delete_one({"_id": session["_id"]})


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not "email" in session or not "privileges" in session:
            return "Session not found", 401
        else:
            return view(**kwargs)
    return wrapped_view


########
# ROUTES
SINCE = datetime.today()


@app.route('/status/about/<string:token>', methods=["GET"])
def status(token):
    if token == ABOUT_TOKEN:
        dt = datetime.today() - SINCE
        sessions = session_db.translator.count_documents({})
        return {"status": "ok", "uptime": f"{dt}", "session_in_db": sessions}, 200
    else:
        return "", 404


@app.route('/webhook', methods=["POST"])
def postJsonHandler():
    return Mwtt.new_event("", request)


@app.route('/', methods=["GET"])
@app.route('/login', methods=["GET"])
@app.route('/select', methods=["GET"])
def login():
    clean_session_db()
    return render_template('index.html')


@app.route('/config/<string:org_id>', methods=["GET"])
def config(org_id):
    return render_template('index.html')


@app.route('/api/login/', methods=["POST"])
def apiLogin():
    return api_login.postApiLogin(request, session)


@app.route('/api/disclaimer/', methods=["GET"])
def apiDisclaimer():
    return api_login.getApiDisclaimer()


@app.route('/api/logout', methods=["POST"])
def logout():
    return api_login.postApiLogout(session)


@app.route('/api/orgs', methods=["GET"])
@login_required
def apiOrgs():
    return api_orgs.apiOrgsGet(session)


@app.route("/api/orgs/settings/<string:org_id>", methods=["GET", "POST", "DELETE"])
@login_required
def apiOrgsSettings(org_id):
    if request.method == "GET":
        return api_orgs.apiOrgsSettingsGet(session, html.escape(org_id), WH_COLLECTOR,  db)
    elif request.method == "POST":
        return api_orgs.apiOrgsSettingsPost(request, session, html.escape(org_id), db)
    elif request.method == "DELETE":
        return api_orgs.apiOrgsSettingsDelete(session, html.escape(org_id), WH_COLLECTOR, db)
    else:
        return "Not Found", 404


@app.route('/api/orgs/webhook/<string:org_id>', methods=["GET", "POST"])
@login_required
def apiOrgWehooks(org_id):
    if request.method == "GET":
        return api_webhooks.apiWebhooksGet(session, html.escape(org_id), WH_COLLECTOR)
    elif request.method == "POST":
        return api_webhooks.apiWebhooksPost(request, session, html.escape(org_id), WH_COLLECTOR, db)


@app.route('/webhooks/<string:org_id>', methods=["POST"])
def whCollector(org_id):
    return collector.whCollectorPost(request, html.escape(org_id), db)


if __name__ == '__main__':
    console.info("Starting Server".center(40, "_"))
    app.run(debug=True, host='0.0.0.0', port=FLASK_PORT)
