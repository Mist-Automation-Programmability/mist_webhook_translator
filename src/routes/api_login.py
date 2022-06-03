import os
import json
from mist import login
from routes.common import extract_json


def postApiLogin(request, session):
    json_data, data = extract_json(request)
    if not json_data:
        return json.dumps({"error": data}), 400
    elif not "username" in data:
        return json.dumps({"username": "email is missing"}), 400
    elif not "password" in data:
        return json.dumps({"error": "password is missing"}), 400
    elif not "host" in data:
        return json.dumps({"error": "host is missing"}), 400
    else:
        host=data["host"]
        username = data["username"]
        password = data["password"]
        two_factor_code = data.get("two_factor_code", "")
        data, code, cookies= login.login(host, username, password, two_factor_code)
        if code == 200 and "privileges" in data:
            session["host"] = host
            session['email'] = data["email"]
            session['privileges'] = data["privileges"]
            session['cookies'] = cookies
        return data, code


def getApiDisclaimer():
    data = {
    "disclaimer": os.environ.get("APP_DISCLAIMER", ""),
    "github_url": os.environ.get("CONFIG.APP_GITHUB_URL", ""),
    "docker_url": os.environ.get("CONFIG.APP_DOCKER_URL", "")
    }
    return json.dumps(data), 200

def postApiLogout(session):
    session.clear()
    return "", 200
