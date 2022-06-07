import json
from routes.common import extract_json, check_privilege
from routes.api_webhooks import apiWebhooksDelete

from mist.topics import topics, topic_names
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


def apiOrgsSettingsGet(session, org_id, WH_COLLECTOR, ORG_SETTINGS):
    console.debug(f"Received new apiOrgsSettingsGet from org {org_id}")
    privilege = check_privilege(session, org_id)
    if not privilege:
        return "Not Found", 404

    try:
        settings = ORG_SETTINGS.get(org_id)
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
            "mist_settings": {"approved_admins": []},
            "topics": {}
        }
    else:
        console.info(
            f"data retrived from DB: Existing settings for org {org_id}")
    return json.dumps({
        "org_id": privilege["org_id"],
        "org_name": privilege["name"],
        "settings": settings,
        "default_topics": topics,
        "url": f"{WH_COLLECTOR}/{org_id}"
    }), 200


def apiOrgsSettingsDelete(session, org_id, WH_COLLECTOR, ORG_SETTINGS):
    console.debug(f"Received new apiOrgsSettingsDelete from org {org_id}")
    privilege = check_privilege(session, org_id)
    if not privilege:
        return "Not Found", 404

    msg, status_code = ORG_SETTINGS.delete(org_id)
    if status_code != 200:
        return msg, status_code
    else:
        return apiWebhooksDelete(session, org_id, WH_COLLECTOR)


def apiOrgsSettingsPost(request, session, org_id, ORG_SETTINGS):

    console.debug(f"Received new apiOrgsSettingsPost from org {org_id}")
    privilege = check_privilege(session, org_id)
    if not privilege:
        return "Not Found", 404

    json_data, data = extract_json(request)
    if not json_data:
        console.error(
            f"Unable to retrieve data from the HTTP Body for org {org_id}")
        return json.dumps({"error": data}), 400

    a,b= ORG_SETTINGS.save(session["host"], org_id, data)
    print(a)
    print(b)
    return a, b
