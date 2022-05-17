from libs import req
import requests
import json


class Slack:

    def __init__(self, config):
        if config:
            self.enabled = config["enabled"]
            self.url = config["url"]
            self.default_url = config["default_url"]
        self.severity = 7

    def _generate_button(self, actions):
        if actions:
            slack_actions = {
                "type": "actions",
                        "elements": []
            }
            i = 0
            for action in actions:
                i += 1
                slack_actions["elements"].append({
                    "type": "button",
                    "text": {
                            "type": "plain_text",
                            "text": action["text"]
                    },
                    "url": action["url"],
                    "action_id": f"{action['tag']}-{i}",
                    "style": "primary"
                }
                )
        else:
            slack_actions = None
        return slack_actions

    def _generate_info(self, info):
        if info:
            slack_info = []

            for elem in info:
                slack_info.append({
                    "type": "context",
                    "elements":[ {
                        "type": "mrkdwn",
                        "text": elem
                    }]
                })
        else:
            slack_info = None
        return slack_info

    def send_manual_message(self, topic, title, text, info=None,  actions=None, channel=None):
        '''
        Send message to Slack Channel

        Params:
            topic   str         Mist webhook topic
            title   str         Message Title
            text    str         Message Text
            info    [str]       Array of info
            actions [obj]       Array of actions {text: btn text, action: btn url, tag: btn id}
            channel str         Slack Channel
        '''
        slack_info = self._generate_info(info)
        slack_button = self._generate_button(actions)
        body = {
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": title
                    }
                }
            ]
        }
        if text:
            body["blocks"].append( {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": text
                    }
                },
                {
                    "type": "divider"
                })
        
        if slack_info:
            for tmp in slack_info:
                body["blocks"].append(tmp)
        if slack_button:
            body["blocks"].append(slack_button)

        if channel and channel in self.url:
            slack_url = self.url[channel]
        else:
            slack_url = self.default_url

        data = json.dumps(body)
        #data = data.encode("ascii")
        # print(slack_url)
        # print(data)
        requests.post(slack_url, headers={
                      "Content-type": "application/json"}, data=data)
