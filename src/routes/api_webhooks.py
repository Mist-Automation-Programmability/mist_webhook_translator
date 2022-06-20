
from mist.webhooks import getWebhooks, deleteWebhook, setWebhook
from routes.common import extract_json, check_privilege
import json
import secrets
from mwtt import Console

console = Console("api_webhook")


def _find_webhook(session, org_id, WH_COLLECTOR):
    webhooks, status_code = getWebhooks(
        session["host"],
        org_id, session["cookies"]
    )
    if not status_code == 200:
        return "Unable to check Webhook configuration in Mist", status_code
    elif webhooks:
        url = f"{WH_COLLECTOR}/{org_id}"
        for webhook in webhooks:
            if webhook.get("url") == url:
                return json.dumps(webhook), 200
    return "", 200


def apiWebhooksGet(session, org_id, WH_COLLECTOR):
    console.debug(f"Received new apiWebhooksGet from org {org_id}")
    privilege = check_privilege(session, org_id)
    if not privilege:
        return "Not Found", 404

    if not "host" in session or not "cookies" in session:
        return "Not Authenticated", 401
    else:
        return _find_webhook(session, org_id, WH_COLLECTOR)


def apiWebhooksPost(request, session, org_id, WH_COLLECTOR,  ORG_SETTINGS):
    console.debug(f"Received new apiWebhooksPost from org {org_id}")
    privilege = check_privilege(session, org_id)
    if not privilege:
        return "Not Found", 404

    json_data, data = extract_json(request)
    if not json_data:
        console.error(f"not able to decode data from org {org_id}")
        return json.dumps({"error": data}), 400
    if type(data.get("topics")) is not list:
        console.error(f"invalid input from org {org_id}")
        return "Invalid input", 400

    console.debug(
        f"tests passed for org {org_id}. retrieving current webhook id")
    webhook, status_code = _find_webhook(session, org_id, WH_COLLECTOR)

    if status_code != 200 and status_code != 404:
        return webhook, status_code
    elif status_code == 200 and webhook:
        console.debug(f"webhook id found for org {org_id}")
        webhook_id = json.loads(webhook)["id"]
    else:
        console.debug(f"no webhook id for org {org_id}")
        webhook_id = None

    if len(data["topics"]) > 0:
        console.debug(f"topic(s) enabled for org {org_id}")
        
        msg, status_code, secret = ORG_SETTINGS.get_webhook_secret(org_id)
        if status_code != 200:
            return msg, status_code
        else:           
            url = f"{WH_COLLECTOR}/{org_id}"
            data = {
                "name": "Mist Webhook Translator",
                "url": url,
                "topics": data["topics"],
                "secret": secret,
                "enabled": True,
                "verify_cert": True,
                "type": "http-post",
                "headers": {}
            }
            return setWebhook(
                session["host"],
                org_id,
                session["cookies"],
                data,
                webhook_id
            )
    else:
        return apiWebhooksDelete(session, org_id,  WH_COLLECTOR)


def apiWebhooksDelete(session, org_id, WH_COLLECTOR):
    console.debug(f"Received new apiWebhooksDelete from org {org_id}")
    privilege = check_privilege(session, org_id)
    if not privilege:
        return "Not Found", 404

    data, status_code = apiWebhooksGet(
        session,
        org_id,
        WH_COLLECTOR
    )
    if status_code != 200 and status_code != 404:
        return data, status_code
    elif status_code == 200 and data:
        console.debug(f"webhook id found for org {org_id}")
        webhook_id = json.loads(data)["id"]
        return deleteWebhook(session["host"], org_id, session["cookies"], webhook_id)
    else:
        console.debug(f"no webhook id for org {org_id}")
        return "Nothing to delete", 200
