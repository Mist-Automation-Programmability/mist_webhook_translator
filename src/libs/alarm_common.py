from datetime import datetime, timedelta


class CommonAlarm():
    '''
    Default Alarm Class used to process Mist Alarm Events

    Parameters:
        mist_host           Mist host (api.mist.com, api.eu.mist.com, ...)
        alarm_channels      Alarm channels from the configuration
        event               Event to process
    '''

    def __init__(self, mist_host, alarm_channels, event):

        self.device_types = {
            "aps": {"short": "AP_", "text": "AP", "insight": "device", "type": "ap"},
            "switches": {"short": "SW_", "text": "Switch", "insight": "juniperSwitch", "type": "switch"},
            "gateways": {"short": "GW_", "text": "Gateway", "insight": "juniperGateway", "type": "gateway"}
        }

        self.event = event
        self.mist_dashboard = mist_host.replace("api", "manage")
        self.org_id = self.event.get("org_id", None)
        self.site_id = self.event.get("site_id", None)
        self.site_name = self.event.get("site_name", None)

        self.count = self.event.get("count", None)
        self.severity = self.event.get("severity")

        self.url = None
        self.channel = None
        self.message = ""

        self.event_id = self.event.get("id", None)
        self.group = self.event.get("group", None)
        self.alarm_type = self.event.get("type", None)
        self.timestamp = self.event.get("timestamp")

        self.switches = self.event.get("switches", None)
        self.gateways = self.event.get("gateways", None)
        self.aps = self.event.get("aps", None)
        self.hostnames = self.event.get("hostnames", None)

        self.title = f"ALARM: {self.alarm_type.replace('_', ' ').upper()}"
        self.text = ""
        self.info = []
        self.actions = []

        d_stop = datetime.now()
        d_start = d_stop - timedelta(days=1)
        self.t_stop = int(datetime.timestamp(d_stop))
        self.t_start = int(datetime.timestamp(d_start))

        self._message_channel(alarm_channels)
        self._actions()
        self._process()

    def get(self):
        '''
        Get the processed information about the event.

        Returns:
            dictionnay with:
                channel     channel applied to this alarm in the config
                title       message title
                text        message text
                info        message additional info
                actions     message buttons
        '''
        return {
            "channel": self.channel,
            "title": self.title,
            "text": self.text,
            "info": self.info,
            "actions": self.actions
        }

    def _message_channel(self, alarm_channels):
        if self.event["type"] in alarm_channels:
            self.channel = alarm_channels[self.event["type"]]

    def _process(self):
        self._common()

    def _common(self):
        '''
        Alarm default processing
        '''
        self.title = f"UNKOWN {self.group} ALARM for site {self.site_name}: {self.alarm_type}"
        for entry in self.event:
            self.info.append(f"{entry.title}: {self.event[entry]}")

    def _alarm_level(self, severity):
        return severity == self.severity

    def _lookup_device_type(self, device_type):
        if device_type in self.event and len(self.event[device_type]) == 1:
            return [self.device_types[device_type], self.event[device_type][0]]
        else:
            return [None, None]

    def _actions(self):
        if self.site_id:
            site_url = f"https://{self.mist_dashboard}/admin/?org_id={self.org_id}#!alerts/site/{self.site_id}/customDate/{self.timestamp}/{self.timestamp}/true/{self._alarm_level('critical')}/{self._alarm_level('warn')}/{self._alarm_level('warn')}/{self.org_id}/{ self._alarm_level('info')}"
            self.actions.append(
                {"tag": "alarm", "text": "See Alarm", "url": site_url})
        else:
            org_url = f"https://{self.mist_dashboard}/admin/?org_id={self.org_id}#!alerts/org/{self.org_id}/customDate/{self.timestamp}/{self.timestamp}/true/{self.group}/{self._alarm_level('critical')}/{self._alarm_level('warn')}/{self._alarm_level('info')}/{self.org_id}"
            self.actions.append(
                {"tag": "alarm", "text": "See Alarm", "url": org_url})

        for device_type in self.device_types:
            device_info, device_id = self._lookup_device_type(device_type)
            if device_info:
                if device_info["insight"] and device_id:
                    url_insights = f"https://{self.mist_dashboard}/admin/?org_id={self.org_id}#!dashboard/insights/{device_info['insight']}/{device_id}/24h/{self.t_start}/{self.t_stop}/{self.site_id}"
                    self.actions.append(
                        {
                            "tag": "insights",
                            "text": f"{device_info['text']} Insights",
                            "url": url_insights}
                    )
                if device_info["type"] and device_id:
                    url_conf = f"https://{self.mist_dashboard}/admin/?org_id={self.org_id}#!{device_info['type']}/detail/{device_id}/{self.site_id}"
                    self.actions.append({
                        "tag": "insights",
                        "text": f"{device_info['text']} Configuration",
                        "url": url_conf
                    })
