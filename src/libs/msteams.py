import requests
import json


color = {
    "audits": "#36a64f",
    "device-events": "#2196f3",
    "device-updowns": "warning",
    "alarms": "danger"
}


def _generage_facts(info):
    if info:
        data_facts =  []
        for data in info:
            data_facts.append({
            "name": "",
            "value": data
        })
    else:
        data_facts = None
    return data_facts

def _generate_button(text, url):
    return {
        "@type": "OpenUri",
        "name": text,
        "targets": [{"os": "default", "uri": url}]
    }

def send_manual_message(config, topic,  title, text, info=None, actions=None, channel=None):
    '''
    Send message to MsTeams Channel

    Params:
        config  obj         Teams URL Configuration {default_url: str, url: {channels: str}}
        topic   str         Mist webhook topic
        title   str         Message Title
        text    str         Message Text
        info    [str]       Array of info
        actions [obj]       Array of actions {text: btn text, action: btn url, tag: btn id}
        channel str         Slack Channel
    '''
    msg_color = color.get(topic, "#eeeeee")
    msteams_actions = []
    for action in actions:
        msteams_actions.append(_generate_button(
            action["text"], action["url"]))

    body = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": msg_color,
        "summary": title,
        "sections": [
            {
                "activityTitle": title,
                "activitySubtitle": text,
                "facts": _generage_facts(info),
                "markdown": True
            }
        ],
        "potentialAction": msteams_actions

    }


    default_url = config.get("default_url", None)
    msteam_url = config.get("url", {}).get(channel, default_url)
    if msteam_url:
        data = json.dumps(body)
        # data = data.encode("ascii")
        # print(msteam_url)
        # print(data)
        requests.post(msteam_url, headers={
                        "Content-type": "application/json"}, data=data)
