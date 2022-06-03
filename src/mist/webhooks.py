import requests
from mwtt import Console

console = Console("mist_webhook")


def _extractAuth(cookies):
    headers = {}
    for cookie in cookies:
        if cookie.name == "csrftoken" and cookie.domain.endswith(".mist.com"):
            headers["X-CSRFToken"] = cookie.value
    return headers


def getWebhooks(host, org_id, cookies):
    url = f"https://{host}/api/v1/orgs/{org_id}/webhooks"
    res = requests.get(
        url,
        cookies=cookies.get_dict()
    )
    if res.status_code == 200:
        console.info(f"Got HTTP{res.status_code} for GET to {url}")
    else:
        console.error(f"Got HTTP{res.status_code} for GET to {url}")
    return res.json(), res.status_code

def setWebhook(host, org_id, cookies, data, webhook_id=None):
    if webhook_id:
        console.debug("webhook_id provided. Routing to update the mist webhook")
        return _updateWebhook(host, org_id, cookies, webhook_id, data)
    else:
        console.debug("no webhook_id provided. Routing to create the mist webhook")
        return _createWebhook(host, org_id, cookies, data)

def _createWebhook(host, org_id, cookies, data):
    url = f"https://{host}/api/v1/orgs/{org_id}/webhooks"
    _extractAuth(cookies)
    res = requests.post(
        url,
        cookies=cookies.get_dict(),
        headers=_extractAuth(cookies),
        json=data
    )
    if res.status_code == 200:
        console.info(f"Got HTTP{res.status_code} for POST to {url}")
    else:
        console.error(f"Got HTTP{res.status_code} for POST to {url}")
    return res.json(), res.status_code


def _updateWebhook(host, org_id, cookies, webhook_id, data):
    url = f"https://{host}/api/v1/orgs/{org_id}/webhooks/{webhook_id}"
    res = requests.put(
        url,
        cookies=cookies.get_dict(),
        headers=_extractAuth(cookies),
        json=data
    )
    if res.status_code == 200:
        console.info(f"Got HTTP{res.status_code} for PUT to {url}")
    else:
        console.error(f"Got HTTP{res.status_code} for PUT to {url}")
    return res.json(), res.status_code


def deleteWebhook(host, org_id, cookies, webhook_id):
    url = f"https://{host}/api/v1/orgs/{org_id}/webhooks/{webhook_id}"
    res = requests.delete(
        url,
        cookies=cookies.get_dict(),
        headers=_extractAuth(cookies),
    )
    if res.status_code == 200:
        console.info(f"Got HTTP{res.status_code} for DELETE to {url}")
    else:
        console.error(f"Got HTTP{res.status_code} for DELETE to {url}")
    return res.json(), res.status_code
