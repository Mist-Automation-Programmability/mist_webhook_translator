from datetime import datetime, timedelta


class CommonAlarm():
    def __init__(self, mist_host, alarm_channels, event):

        self.device_types = {"aps": {"short": "AP_", "text": "AP", "insight": "device", "type": "ap"},
                             "switches": {"short": "SW_", "text": "Switch", "insight": "juniperSwitch", "type": "switch"},
                             "gateways": {"short": "GW_", "text": "Gateway", "insight": "juniperGateway", "type": "gateway"}}

        self.event = event

        self.org_id = None
        self.site_id = None

        self.url = None
        self.text = []
        self.actions = []
        self.channel = None
        self.message = ""

        self.alarm_type = "any%20type"
        self.severity = ""
        self.timestamp = ""
        self.switches = None
        self.gateways = None
        self.aps = None
        self.event_id = ""
        self.group = ""

        d_stop = datetime.now()
        d_start = d_stop - timedelta(days=1)
        self.t_stop = int(datetime.timestamp(d_stop))
        self.t_start = int(datetime.timestamp(d_start))

        self._message_channel(alarm_channels)
        self._extract_fields()
        self._actions(mist_host)
        self._process()

    def get(self):
        return [self.channel, self.text, self.actions]

    def _message_channel(self, alarm_channels):
        if self.event["type"] in alarm_channels:
            self.channel = alarm_channels[self.event["type"]]

    def _extract_fields(self):
        if "severity" in self.event:
            self.severity = self.event["severity"]
        if "timestamp" in self.event:
            self.timestamp = self.event["timestamp"]
        if "org_id" in self.event:
            self.org_id = self.event["org_id"]
        if "site_id" in self.event:
            self.site_id = self.event["site_id"]
        if "switches" in self.event:
            self.switches = self.event["switches"]
        if "gateways" in self.event:
            self.gateways = self.event["gateways"]
        if "aps" in self.event:
            self.aps = self.event["aps"]
        if "id" in self.event:
            self.event_id = self.event["id"]
        if "group" in self.event:
            self.group = self.event["group"]
        if "type" in self.event:
            self.alarm_type = self.event["type"]

    def _process(self):
        self._common()
        
    def _common(self):
        for entry in self.event:
            self.text.append("{0}: {1}".format(
                entry.title(), self.event[entry]))

    def _alarm_level(self, severity):
        return severity == self.severity

    def _lookup_device_type(self, device_type):
        if device_type in self.event and len(self.event[device_type]) == 1:
            return [self.device_types[device_type], self.event[device_type][0]]
        else:
            return [None, None]

    def _actions(self, mist_host):
        host = mist_host.replace("api", "manage")
        if self.site_id:
            site_url = "https://{0}/admin/?org_id={1}#!alerts/site/{2}/customDate/{3}/{3}/true/{4}/{5}/{6}/{7}/{2}".format(
                host, self.org_id, self.site_id, self.timestamp, self.group, self._alarm_level("critical"), self._alarm_level("warn"), self._alarm_level("info"))
            self.actions.append(
                {"tag": "alarm", "text": "See Alarm", "url": site_url})
        else:
            org_url = "https://{0}/admin/?org_id={1}#!alerts/org/{1}/customDate/{2}/{2}/true/{3}/{4}/{5}/{6}/{1}".format(
                host, self.org_id, self.timestamp, self.group, self._alarm_level("critical"), self._alarm_level("warn"), self._alarm_level("info"))
            self.actions.append(
                {"tag": "alarm", "text": "See Alarm", "url": org_url})

        for device_type in self.device_types:
            device_info, device_id = self._lookup_device_type(device_type)
            if device_info:
                if device_info["insight"] and device_id:
                    url_insights = "https://{0}/admin/?org_id={1}#!dashboard/insights/{2}/{3}/24h/{4}/{5}/{6}".format(
                        host, self.org_id, device_info["insight"], device_id, self.t_start, self.t_stop, self.site_id)
                    self.actions.append(
                        {"tag": "insights", "text": "{0} Insights".format(device_info["text"]), "url": url_insights})
                if device_info["type"] and device_id:
                    url_conf = "https://{0}/admin/?org_id={1}#!{2}/detail/{3}/{4}".format(
                        host, self.org_id, device_info["type"], device_id, self.site_id)
                    self.actions.append(
                        {"tag": "insights", "text": "{0} Configuration".format(device_info["text"]), "url": url_conf})
