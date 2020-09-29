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
            "green": "#36a64f",
            "blue": "#2196f3",
            "orange": "warning",
            "red": "danger"

        }

    def _get_color(self):
        if self.severity >= 6:
            return self.color["green"]
        elif self.severity >= 5:
            return self.color["blue"]
        elif self.severity >= 4:
            return self.color["orange"]
        else:
            return self.color["red"]

    def _generate_button(self, text, url):
        return {
                "@type": "OpenUri",
                "name": text,
                "targets": [{"os": "default", "uri": url}]
            }   

    def send_manual_message(self, title, subtitle, text=[], channel=None, color="eee", actions=[]):
        facts = []
        for tpart in text:
            name = tpart.split(":")[0]
            value = ":".join(tpart.split(":")[1:]).strip()
            facts.append({"name": name, "value": value})

        msteams_actions = []
        for action in actions:
            msteams_actions.append(self._generate_button(
                action["text"], action["url"]))

        body = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": color,
            "summary": title,
            "sections": [{
                "activityTitle": title,
                "activitySubtitle": subtitle,
                "facts": facts,
                "markdown": False
            }],
            "potentialAction": msteams_actions
            
        }

        if channel and channel in self.url:
            msteam_url = self.url[channel]
        else:
            msteam_url = self.default_url
        
        data = json.dumps(body)
        data = data.encode("ascii")
        
        requests.post(msteam_url, headers={
                      "Content-type": "application/json"}, data=data)
