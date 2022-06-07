import json
from routes.common import extract_json, check_privilege
from routes.api_webhooks import apiWebhooksDelete
from mist.topics import topics, topic_names
import bson.json_util as json_util

from mwtt import Console

console = Console("api_orgs")


def apiOrgsGet(session):
    console.debug("Received new apiOrgsGet")
    data = []
    for privilege in session["privileges"]:
        if privilege.get("scope") == "org" and privilege.get("role") == "admin":
            name = privilege["name"]
            if privilege.get("msp_name"):
                name += f" ({privilege['msp_name']})"
            data.append({"name": name, "org_id": privilege["org_id"]})
    data = sorted(data, key=lambda o: o["name"])
    return json.dumps(data), 200


def apiOrgsSettingsGet(session, org_id, WH_COLLECTOR, db):
    console.debug(f"Received new apiOrgsSettingsGet from org {org_id}")
    privilege = check_privilege(session, org_id)
    if not privilege:
        return "Not Found", 404

    try:
        settings = db["settings"].find_one({"org_id": org_id})
        settings = json.loads(json_util.dumps(settings))
    except:
        console.error(
            f"Unable to retrive settings from DB for the org {org_id}")
        return "", 500

    if not settings:
        console.info(f"data retrived from DB: New settings for org {org_id}")
        topics_status = {}
        for topic in topic_names:
            topics_status[topic] = False
        settings = {
            "slack_settings": {},
            "teams_settings": {},
            "topics_status": topics_status,
            "topics": {}
        }
    else:
        console.info(
            f"data retrived from DB: Existing settings for org {org_id}")
        del settings["_id"]
    return json.dumps({
        "org_id": privilege["org_id"],
        "org_name": privilege["name"],
        "settings": settings,
        "default_topics": topics,
        "url": f"{WH_COLLECTOR}/{org_id}"
    }), 200


def apiOrgsSettingsDelete(session, org_id, WH_COLLECTOR, db):
    console.debug(f"Received new apiOrgsSettingsDelete from org {org_id}")
    privilege = check_privilege(session, org_id)
    if not privilege:
        return "Not Found", 404

    try:
        db["settings"].delete_one({"org_id": org_id})
        console.error(f"Settings deleted for org {org_id}")
        return apiWebhooksDelete(session, org_id, WH_COLLECTOR)
    except:
        console.error(
            f"Error when deleting the configuration for org {org_id}")
        return "Error when deleting the configuration", 500


def apiOrgsSettingsPost(request, session, org_id, db):

    console.debug(f"Received new apiOrgsSettingsPost from org {org_id}")
    privilege = check_privilege(session, org_id)
    if not privilege:
        return "Not Found", 404

    json_data, data = extract_json(request)
    if not json_data:
        console.error(
            f"Unable to retrieve data from the HTTP Body for org {org_id}")
        return json.dumps({"error": data}), 400

    secured_data = {
        "topics_status": {},
        "topics": {},
        "slack_settings": {"enabled": False, "url": {}},
        "teams_settings": {"enabled": False, "url": {}},
        "mist_settings": {"mist_host": "", "secret": "", "approved_admins": []}
    }

    if type(data.get("topics_status") is dict):
        for entry in data["topics_status"]:
            if entry in topic_names and type(data["topics_status"][entry]) is bool:
                secured_data["topics_status"][entry] = data["topics_status"][entry]

    if type(data.get("topics")) is list:
        for entry in data["topics"]:
            if type(entry.get("topic")) is str \
                    and type(entry.get("topic")) is str \
                    and type(entry.get("name")) is str \
                    and type(entry.get("channel")) is str \
                    and entry["topic"] in topic_names:
                if not entry["topic"] in secured_data["topics"]:
                    secured_data["topics"][entry["topic"]] = {}
                secured_data["topics"][entry["topic"]
                                       ][entry["name"]] = entry["channel"]

    if type(data.get("slack_settings")) is dict:
        if type(data["slack_settings"].get("enabled")) is bool:
            secured_data["slack_settings"]["enabled"] = data["slack_settings"]["enabled"]
        if type(data["slack_settings"].get("url")) is dict:
            for channel in data["slack_settings"]["url"]:
                if type(data["slack_settings"]["url"][channel]) is str:
                    secured_data["slack_settings"]["url"][channel] = data["slack_settings"]["url"][channel]

    if type(data.get("teams_settings")) is dict:
        if type(data["teams_settings"].get("enabled")) is bool:
            secured_data["teams_settings"]["enabled"] = data["teams_settings"]["enabled"]
        if type(data["teams_settings"].get("url")) is dict:
            for channel in data["teams_settings"]["url"]:
                if type(data["teams_settings"]["url"][channel]) is str:
                    secured_data["teams_settings"]["url"][channel] = data["teams_settings"]["url"][channel]

    if type(data.get("approved_admins")) is list:
        for admin in data["approved_admins"]:
            if type(admin) is list:
                secured_data["mist_settings"]["approved_admins"].append(admin)

    secured_data["mist_settings"]["mist_host"] = session["host"]
    secured_data["org_id"] = org_id
    console.debug(f"received data cleaned for org {org_id}")

    try:
        current_settings = db["settings"].find_one({"org_id": org_id})
    except:
        console.error(f"Unable to retrive data for the org {org_id}")

    if not current_settings:
        try:
            res = db["settings"].insert_one(secured_data)
            console.info(f"New org {org_id} created")
            return "", 200
        except:
            console.error(f"Unable to create new org {org_id}")
            return "Error when saving data", 500
    else:
        try:
            secured_data["mist_settings"]["secret"] = current_settings["mist_settings"]["secret"]
            res = db["settings"].update(
                {"_id": current_settings["_id"]}, {"$set": secured_data})
            if res["ok"] == 1:
                console.info(f"data updated for org {org_id}")
                return "", 200
            else:
                console.error(f"unable to update data for org {org_id}")
                return "", 500
        except:
            console.error(f"Error when saving data for org {org_id}")
            return "Error when saving data", 500
