from datetime import datetime, timedelta


class CommonEvent():

    def __init__(self, mist_host, event_channels, event):
        self.event = event
        self.org_id = None

        self.site_id = None
        self.site_name = None

        self.device_id = ""
        self.device_name = ""
        self.device_mac = ""

        self.audit_id = None

        self.text = []
        self.actions = []
        self.channel = None
        self.reason = None

        self.device_type = ""
        self.device_text = "Device"
        self.device_short = ""
        self.device_insight = ""

        self.device_types = {"ap": {"short": "AP_", "text": "AP", "insight": "device"},
                        "switch": {"short": "SW_", "text": "Switch", "insight": "juniperSwitch"},
                        "gateway": {"short": "GW_", "text": "Gateway", "insight": "juniperGateway"}}

        d_stop = datetime.now()
        d_start = d_stop - timedelta(days=1)
        self.t_stop = int(datetime.timestamp(d_stop))
        self.t_start = int(datetime.timestamp(d_start))

        self._message_channel(event_channels)
        self._extract_fields()
        self._actions(mist_host)
        self._process()

    def get(self):
        return [self.channel, self.text, self.actions]

    def _message_channel(self, event_channels):
        if self.event["type"] in event_channels:
            self.channel = event_channels[self.event["type"]]

    def _extract_fields(self):
        if "org_id" in self.event:
            self.org_id = self.event["org_id"]
        if "site_id" in self.event:
            self.site_id = self.event["site_id"]
        if "mac" in self.event:
            self.device_mac = self.event["mac"]
            self.device_id = "00000000-0000-0000-1000-%s" % (self.device_mac)
        elif "ap" in self.event:
            self.device_mac = self.event["ap"]
            self.device_id = "00000000-0000-0000-1000-%s" % (self.device_mac)
        if "device_name" in self.event:
            self.device_name = self.event["device_name"]
        elif "ap_name" in self.event:
            self.device_name = self.event["ap_name"]
        if "site_name" in self.event:
            self.site_name = self.event["site_name"]
        if "type" in self.event:
            self.event_type = self.event["type"]
        if "device_type" in self.event:
            self.device_type = self.event["device_type"]
            if self.device_type in self.device_types:
                self.device_text = self.device_types[self.device_type]["text"]
                self.device_short = self.device_types[self.device_type]["short"]
                self.device_insight = self.device_types[self.device_type]["insight"]
        if "reason" in self.event:
            self.reason = self.event["reason"]
        if "audit_id" in self.event:
            self.audit_id = self.event["audit_id"]
        if "text" in self.event:
            self.event_text = self.event["text"]

    def _actions(self, mist_host):
        if self.device_type:
            if self.audit_id:
                self.text.append("Check the audit logs for more details.")

            if "audit_id" in self.event:
                host = mist_host.replace("api", "manage")
                url_audit = "https://{0}/admin/?org_id={1}#!auditLogs".format(
                    host, self.org_id)
                self.actions.append(
                    {"tag": "audit", "text": "Audit Logs", "url": url_audit})
            if not self.event["type"].replace(self.device_type, "") == "UNASSIGNED":
                if self.device_insight:
                    url_insights = "https://{0}/admin/?org_id={1}#!dashboard/insights/{2}/{3}/24h/{4}/{5}/{6}".format(
                        host, self.org_id, self.device_insight, self.device_id, self.t_start, self.t_stop, self.site_id)
                    self.actions.append(
                        {"tag": "insights", "text": "{0} Insights".format(self.device_text), "url": url_insights})
                if self.device_type:
                    url_conf = "https://{0}/admin/?org_id={1}#!{2}/detail/{3}/{4}".format(
                        host, self.org_id, self.device_type, self.device_id, self.site_id)
                    self.actions.append(
                        {"tag": "insights", "text": "{0} Configuration".format(self.device_text), "url": url_conf})

    def _process(self):
        self.text.append("Device Name: %s" % (self.device_name))
        self.text.append("Device MAC: %s" % (self.device_mac))
        self.text.append("Site: %s" % (self.site_name))
        self.text.append("Event: %s" % (self.event_type))
        self.text.append("Reason: %s" % (self.reason))

    def _assigned(self):
        '''
    19/05/2020 00:21:04 INFO: device-events
    19/05/2020 00:21:04 INFO: ap: d420b0002e95
    19/05/2020 00:21:04 INFO: device_name: ap-41.off.lab
    19/05/2020 00:21:04 INFO: org_id: 203d3d02-dbc0-4c1b-9f41-76896a3330f4
    19/05/2020 00:21:04 INFO: reason: scheduled-site-rrm
    19/05/2020 00:21:04 INFO: site_id: fa018c13-008b-46ae-aa18-1eeb894a96c4
    19/05/2020 00:21:04 INFO: site_name: lab
    19/05/2020 00:21:04 INFO: timestamp: 1589847656
    19/05/2020 00:21:04 INFO: type: 1026
        '''
        text_string = "{0} \"{1}\" (MAC: {2}) is assigned".format(
            self.device_text, self.device_name, self.device_mac)
        if self.site_name:
            text_string += " to site \"{0}\" ".format(self.site_name)
        text_string += "."
        self.text.append(text_string)

    def _unassigned(self):
        '''
    20/05/2020 12:57:21 INFO: device-events
    20/05/2020 12:57:21 INFO: ap: 5c5b351ef069
    20/05/2020 12:57:21 INFO: device_name: bt-11.ktc.lab
    20/05/2020 12:57:21 INFO: audit_id: 38aaf359-5c60-4ed8-9c08-04a9a244e478
    20/05/2020 12:57:21 INFO: org_id: 203d3d02-dbc0-4c1b-9f41-76896a3330f4
    20/05/2020 12:57:21 INFO: site_id: fa018c13-008b-46ae-aa18-1eeb894a96c4
    20/05/2020 12:57:21 INFO: site_name: test_only_1
    20/05/2020 12:57:21 INFO: text: AP 5c5b351ef069 unassigned
    20/05/2020 12:57:21 INFO: timestamp: 1589979432
    20/05/2020 12:57:21 INFO: type: AP_UNASSIGNED
        '''
        text_string = "{0} \"{1}\" (MAC: {2}) is unassigned".format(
            self.device_text, self.device_name, self.device_mac)
        # if site_name:
        #    text_string += " from site %s" %(site_name)
        text_string += "."
        self.text.append(text_string)

    def _upgrade_by_user(self):
        '''
    07/08/2020 08:14:23 INFO: device-events
    07/08/2020 08:14:23 INFO: ap: d420b0002e95
    07/08/2020 08:14:23 INFO: device_name: ap41-off.lab
    07/08/2020 08:14:23 INFO: audit_id: 3ef223c8-2308-4040-a8f7-dbe5a96d8890
    07/08/2020 08:14:23 INFO: org_id: 203d3d02-dbc0-4c1b-9f41-76896a3330f4
    07/08/2020 08:14:23 INFO: site_id: f5fcbee5-fbca-45b3-8bf1-1619ede87879
    07/08/2020 08:14:23 INFO: site_name: lab
    07/08/2020 08:14:23 INFO: timestamp: 1596788059
    07/08/2020 08:14:23 INFO: type: AP_UPGRADE_BY_USER
        '''
        text_string = "{0} \"{1}\" (MAC: {2}): Firmware upgrade requested".format(
            self.device_text, self.device_name, self.device_mac)
        # if site_name:
        #    text_string += " from site %s" %(site_name)
        text_string += "."
        self.text.append(text_string)

    def _upgraded(self):
        '''
    07/08/2020 08:14:53 INFO: device-events
    07/08/2020 08:14:53 INFO: ap: d420b0002e95
    07/08/2020 08:14:53 INFO: device_name: ap41-off.lab
    07/08/2020 08:14:53 INFO: audit_id: 3ef223c8-2308-4040-a8f7-dbe5a96d8890
    07/08/2020 08:14:53 INFO: org_id: 203d3d02-dbc0-4c1b-9f41-76896a3330f4
    07/08/2020 08:14:53 INFO: site_id: f5fcbee5-fbca-45b3-8bf1-1619ede87879
    07/08/2020 08:14:53 INFO: site_name: lab
    07/08/2020 08:14:53 INFO: text: from version 0.7.20141 to 0.7.20216
    07/08/2020 08:14:53 INFO: timestamp: 1596788089
    07/08/2020 08:14:53 INFO: type: AP_UPGRADED
        '''
        text_string = "{0} \"{1}\" (MAC: {2}): Firmware upgrade finished {3}".format(
            self.device_text, self.device_name, self.device_mac, self.event_text)
        # if site_name:
        #    text_string += " from site %s" %(site_name)
        text_string += "."
        self.text.append(text_string)

    def _common(self):
        '''
    20/05/2020 06:30:54 INFO: device-events
    20/05/2020 06:30:54 INFO: ap: d420b0002e95
    20/05/2020 06:30:54 INFO: device_name: ap-41.off.lab
    20/05/2020 06:30:54 INFO: org_id: 203d3d02-dbc0-4c1b-9f41-76896a3330f4
    20/05/2020 06:30:54 INFO: site_id: fa018c13-008b-46ae-aa18-1eeb894a96c4
    20/05/2020 06:30:54 INFO: site_name: lab
    20/05/2020 06:30:54 INFO: timestamp: 1589956243
    20/05/2020 06:30:54 INFO: type: AP_CONFIGURED
        '''
        text_string = "{0} \"{1}\" (MAC: {2}) ".format(
            self.device_text, self.device_name, self.device_mac)
        if self.site_name:
            text_string += "on site \"{0}\" ".format(self.site_name)

        event_type = self.event_type
        for device_type in self.device_types:
            if self.event_type.startswith(self.device_types[device_type]["short"]):
                event_type = self.event_type.replace("{0}".format(self.device_types[device_type]["short"]), "").title()
        text_string += "is {0}.".format(event_type)
        self.text.append(text_string)

    def _config_changed_by_user(self):
        '''
    19/05/2020 07:16:11 INFO: device-events
    19/05/2020 07:16:11 INFO: ap: d420b0002e95
    19/05/2020 07:16:11 INFO: device_name: ap-41.off.lab
    19/05/2020 07:16:11 INFO: audit_id: b2b06f12-02f1-48d7-9682-f82766c4002c
    19/05/2020 07:16:11 INFO: org_id: 203d3d02-dbc0-4c1b-9f41-76896a3330f4
    19/05/2020 07:16:11 INFO: site_id: fa018c13-008b-46ae-aa18-1eeb894a96c4
    19/05/2020 07:16:11 INFO: site_name: lab
    19/05/2020 07:16:11 INFO: timestamp: 1589872563
    19/05/2020 07:16:11 INFO: type: AP_CONFIG_CHANGED_BY_USER
        '''
        text_string = "Configuration for {0} \"{1}\" (MAC: {2})".format(
            self.device_text, self.device_name, self.device_mac)
        if self.site_name:
            text_string += " on site \"%s\"" % (self.site_name)
        text_string += " is changed by User."
        self.text.append(text_string)

    def _unclaimed(self):
        '''
    10/08/2020 07:56:43 INFO: device-events
    10/08/2020 07:56:43 INFO: ap: d420b0002d5f
    10/08/2020 07:56:43 INFO: audit_id: 341e2c5d-db35-44ce-97c9-fcdbd5d1bdb3
    10/08/2020 07:56:43 INFO: org_id: 203d3d02-dbc0-4c1b-9f41-76896a3330f4
    10/08/2020 07:56:43 INFO: text: AP d420b0002d5f unclaimed
    10/08/2020 07:56:43 INFO: timestamp: 1597046195
    10/08/2020 07:56:43 INFO: type: AP_UNCLAIMED
        '''
        text_string = "{0} \"{1}\" (MAC: {2}) has been Unclaimed".format(
            self.device_text, self.device_name, self.device_mac)
        self.text.append(text_string)

    def _claimed(self):
        '''
    10/08/2020 14:36:33 INFO: device-events
    10/08/2020 14:36:33 INFO: ap: 5c5b351f1bed
    10/08/2020 14:36:33 INFO: device_name: 5c5b351f1bed
    10/08/2020 14:36:33 INFO: audit_id: 7b377bc3-20f8-4184-b6fe-de6709f73f00
    10/08/2020 14:36:33 INFO: org_id: 203d3d02-dbc0-4c1b-9f41-76896a3330f4
    10/08/2020 14:36:33 INFO: site_name: test_only
    10/08/2020 14:36:33 INFO: text: AP 5c5b351f1bed claimed
    10/08/2020 14:36:33 INFO: timestamp: 1597070182
    10/08/2020 14:36:33 INFO: type: AP_CLAIMED
        '''
        text_string = "{0} \"{1}\" (MAC: {2}) has been Claimed".format(
            self.device_text, self.device_name, self.device_mac)
        if self.site_name:
            text_string += " on site \"{0}\" ".format(self.site_name)
        self.text.append(text_string)
