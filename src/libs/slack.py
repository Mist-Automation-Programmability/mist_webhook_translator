from libs import req
import requests
import json
import time
from datetime import datetime
class Slack:

    def __init__(self, config):
        if config: 
            self.enabled = config["enabled"]
            self.url = config["url"]
        self.severity = 7
        self.color ={
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


    def send_manual_message(self, title, message, color=None):
        if not color: color = self.color["green"]
        now = datetime.now()
        now.strftime("%d/%m/%Y %H:%M:%S")
        title = "%s - %s" %(now, title)
        
        body = {
            "attachments": [
                {
                    "fallback": "New MWTS event",
                    "color": color,
                    "pretext": title,          
                    "text": message,            
                }
            ]
        }
        
        data = json.dumps(body)
        data = data.encode("ascii")
        requests.post(self.url, headers={"Content-type": "application/json"}, data=data)
        
