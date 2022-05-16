from libs import req
import requests
import json


class Teams:

    def __init__(self, config):
        if config:
            self.enabled = config["enabled"]
            self.url = config["url"]
            self.default_url = config["default_url"]
        self.severity = 7
        self.color = {
            "audit": "#36a64f",
            "device-events": "#2196f3",
            "device-updowns": "warning",
            "alarm": "danger"

        }


    def _generage_facts(self, info):
        if info:
            data_facts =  []
            for data in info:
                data_facts.append({
                "name": "info",
                "value": data
            })
        else:
            data_facts = None
        return data_facts

    def _generate_button(self, text, url):
        return {
            "@type": "OpenUri",
            "name": text,
            "targets": [{"os": "default", "uri": url}]
        }

    def send_manual_message(self, topic,  title, text, info=None, actions=None, channel=None):
        '''
        Send message to MsTeams Channel

        Params:
            topic   str         Mist webhook topic
            title   str         Message Title
            text    str         Message Text
            info    [str]       Array of info
            actions [obj]       Array of actions {text: btn text, action: btn url, tag: btn id}
            channel str         Slack Channel
        '''
        color = self.color[topic]
        msteams_actions = []
        for action in actions:
            msteams_actions.append(self._generate_button(
                action["text"], action["url"]))

        body = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": color,
            "summary": title,
            "sections": [
                {
                    "activityTitle": title,
                    "activitySubtitle": text,
                    "facts": self._generage_facts(info),
                    "markdown": True
                }
            ],
            "potentialAction": msteams_actions

        }

        if channel and channel in self.url:
            msteam_url = self.url[channel]
        else:
            msteam_url = self.default_url

        data = json.dumps(body)
        # data = data.encode("ascii")
        # print(data)
        requests.post(msteam_url, headers={
                      "Content-type": "application/json"}, data=data)
