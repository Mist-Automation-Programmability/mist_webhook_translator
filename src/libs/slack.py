from libs import req
import requests
import json


class Slack:

    def __init__(self, config):
        if config:
            self.enabled = config["enabled"]
            self.url = config["url"]            
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

    def _generate_button(self, tag, text, url):
        return {
                    "name": tag,
					"type": "button",
					"text": {
						"text": text
					},
					"style": "primary",
					"url": url
				}

    def _generate_attachments(self, text, color, actions=None):
            return [{
                "fallback": "New MWTT event",
                "color": color,
                "text": text,
                "attachment_type": "default",
                "actions": actions
            }]

    def send_manual_message(self, title, text=[], level='unknown', color="eee", actions=[]):
        slack_text = ""
        for tpart in text:
            slack_text+="%s\r" %(tpart)

        slack_actions = []
        for action in actions:
            slack_actions.append(self._generate_button(action["tag"], action["text"], action["url"]))

        attachments = self._generate_attachments(slack_text, color, slack_actions)

        body = {
            "text": title,
            "attachments": attachments
        }

        if level in self.url:
            slack_url = self.url[level]
        else: 
            slack_url = self.url["unknown"]

        data = json.dumps(body)
        data = data.encode("ascii")

        print("- slack -")
        print(slack_url)
        print(data)
        print("- msteams -")

        requests.post(slack_url, headers={
                      "Content-type": "application/json"}, data=data)
