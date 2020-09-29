from datetime import datetime, timedelta
from .alarm_common import CommonAlarm


class InfraAlarm(CommonAlarm):

    def __init__(self, mist_host, alarm_channels, event):
        CommonAlarm.__init__(self, mist_host, alarm_channels, event)


    def _process(self):
        if self.alarm_type in ["device_down", "device_down", "device_down"]:
            self._down()
        elif self.alarm_type in ["device_restarted", "device_restarted", "device_restarted"]:
            self._restarted()
        else:
            self._common()

    def _get_device_string(self):
        text_string = "Device(s)"
        if "aps" in self.event:
            if "count" in self.event and self.event.count > 1:
                text_string = "{0} APs".format(self.event.count)
            elif "count" in self.event:
                text_string = "{0} AP".format(self.event.count)
            else:
                text_string = "AP(s)"
        elif "gateways" in self.event:
            if "count" in self.event and self.event.count > 1:
                text_string = "{0} Gateways".format(self.event.count)
            elif "count" in self.event:
                text_string = "{0} Gateway".format(self.event.count)
            else:
                text_string = "Gateway(s)"
        elif "switches" in self.event:
            if "count" in self.event and self.event.count > 1:
                text_string = "{0} Switches".format(self.event.count)
            elif "count" in self.event:
                text_string = "{0} Switch".format(self.event.count)
            else:
                text_string = "Switch(es)"
        return text_string

    def _down(self):
        """
            "severity": "warn",
            "timestamp": 1601362414,
            "last_seen": 1601362414,
            "aps": [
                "d420b0002e95"
            ],
            "org_id": "203d3d02-dbc0-4c1b-9f41-76896a3330f4",
            "site_id": "e7006522-6b29-4610-a367-1b6568a9d98c",
            "count": 1.0,
            "id": "e13213e8-5aa5-48f4-90bb-bfbad0dc8dfd",
            "type": "device_down",
            "group": "infrastructure"
        },
        """
        text_string = self._get_device_string()
        text_string += " down"
        if "timestamp" in self.event: text_string += " at {0}".format(datetime.fromtimestamp(self.event["timestamp"]))           
        self.text.append(text_string)

    def _restarted(self):
        """
                {
            "severity": "info",
            "timestamp": 1601320971,
            "last_seen": 1601320971,
            "aps": [
                "d420b0002e95"
            ],
            "org_id": "203d3d02-dbc0-4c1b-9f41-76896a3330f4",
            "site_id": "e7006522-6b29-4610-a367-1b6568a9d98c",
            "count": 1.0,
            "id": "bcdf8217-2eda-4d62-8976-af1f64936c76",
            "type": "device_restarted",
            "group": "infrastructure"
        },
        """
        text_string = self._get_device_string()
        text_string += " restarted"
        if "timestamp" in self.event: text_string += " at {0}".format(datetime.fromtimestamp(self.event["timestamp"]))           
        self.text.append(text_string)