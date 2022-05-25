from datetime import datetime, timedelta
from .logger import Console


class CommonEvent():
    '''
    Default Event Class used to process Mist Alarm Events

    Parameters:
        mist_host           Mist host (api.mist.com, api.eu.mist.com, ...)
        alarm_channels      Event channels from the configuration
        event               Event to process
    '''

    def __init__(self, mist_host, event_channels, event):
        self.console = Console("event")
        self.device_types = {
            "ap": {"short": "AP_", "text": "AP", "insight": "device"},
            "switch": {"short": "SW_", "text": "Switch", "insight": "juniperSwitch"},
            "gateway": {"short": "GW_", "text": "Gateway", "insight": "juniperGateway"},
            "mxedge": {"short": "ME_", "text": "Mist Edge", "insight": "mxedge"}
        }
        self.event = event
        self.mist_dashboard = mist_host.replace("api", "manage")

        self.org_id = self.event.get("org_id", None)
        self.site_id = self.event.get("site_id", None)
        self.site_name = self.event.get("site_name", None)

        self.device_name = self.event.get("device_name", None)
        self.device_mac = self.event.get("mac", None)
        if self.device_mac:
            self.device_id = f"00000000-0000-0000-1000-{self.device_mac}"

        self.audit_id = self.event.get("audit_id", None)

        self.event_text = self.event.get("text", None)
        self.channel = None
        self.reason = self.event.get("reason", None)
        self.event_type = self.event.get("type", None)

        self.model = self.event.get("model", None)
        self.version = self.event.get("version", None)
        self.device_type = self.event.get("device_type", None)

        if self.device_type not in self.device_types:
            self.device_text = "Device"
            self.device_short = ""
            self.device_insight = ""
        else:
            self.device_text = self.device_types[self.device_type]["text"]
            self.device_short = self.device_types[self.device_type]["short"]
            self.device_insight = self.device_types[self.device_type]["insight"]

        self.title = f"EVENT: {self.event_type.replace('_', ' ')}"
        self.text = ""
        self.info = []
        if self.event_text:
            self.info.append(self.event_text)
        if self.reason:
            self.info.append(f"*Reason*: {self.reason}")
        if self.model:
            self.info.append(f"*Model*: {self.model}")
        if self.version:
            self.info.append(f"*Version*: {self.version}")
        self.actions = []

        d_stop = datetime.now()
        d_start = d_stop - timedelta(days=1)
        self.t_stop = int(datetime.timestamp(d_stop))
        self.t_start = int(datetime.timestamp(d_start))

        self._message_channel(event_channels)
        # self._text()
        self._process()
        self._actions()

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
        data = {
            "channel": self.channel,
            "title": self.title,
            "text": self.text,
            "info": self.info,
            "actions": self.actions
        }
        self.console.info("Processing done")
        self.console.debug(f"Result: {data}")
        return data

    def _process(self):
        self._common()

    def _message_channel(self, event_channels):
        if self.event["type"] in event_channels:
            self.channel = event_channels[self.event["type"]]

    def _actions(self):
        if self.device_type:
            if self.audit_id:
                self.info.append("Check the audit logs for more details.")

            if "audit_id" in self.event:
                url_audit = f"https://{self.mist_dashboard}/admin/?org_id={self.org_id}#!auditLogs"
                self.actions.append(
                    {"tag": "audit", "text": "Audit Logs", "url": url_audit})
            if not self.event["type"].replace(self.device_type, "") == "UNASSIGNED":
                if self.device_insight:
                    url_insights = f"https://{self.mist_dashboard}/admin/?org_id={self.org_id}#!dashboard/insights/{self.device_insight}/{self.device_id}/24h/{self.t_start}/{self.t_stop}/{self.site_id}"
                    self.actions.append({
                        "tag": "insights",
                        "text": f"{self.device_text} Insights",
                        "url": url_insights
                    })
                if self.device_type:
                    url_conf = f"https://{self.mist_dashboard}/admin/?org_id={self.org_id}#!{self.device_type}/detail/{self.device_id}/{self.site_id}"
                    self.actions.append({
                        "tag": "insights",
                        "text": f"{self.device_text} Configuration",
                        "url": url_conf
                    })

    def _common(self):
        '''
        Event default processing
        '''
        for entry in self.event:
            self.info.append(f"*{entry}*: {self.event[entry]}")

    def _claimed(self):
        '''
{
    "type": "AP_CLAIMED",
    "timestamp": 1552408871,
    "org_id": "2818e386-8dec-2562-9ede-5b8a0fbbdc71",
    "site_id": "4ac1dcf4-9d8b-7211-65c4-057819f0862b",
    "ap": "5c5b35000001",
    "audit_id": "e9a88814-fa81-5bdc-34b0-84e8735420e5"
}
        '''
        self.text = f"{self.device_text} \"{self.device_name}\" (MAC: {self.device_mac}) has been {self.event_type.split('_')[1]}"
        if self.site_name:
            self.text += f" to site \"{self.site_name}\""

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
        self.text = f"{self.device_text} \"{self.device_name}\" (MAC: {self.device_mac}) ASSIGNED"
        if self.site_name:
            self.text += f" to site \"{self.site_name}\""

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
        self.text = f"{self.device_text} \"{self.device_name}\" (MAC: {self.device_mac}) has been {self.event_type.split('_')[1]}"
        if self.site_name:
            self.text += f" from site \"{self.site_name}\""

    def _connected(self):
        '''
    19/05/2020 07:16:11 INFO: device-events
    19/05/2020 07:16:11 INFO: ap: d420b0002e95
    19/05/2020 07:16:11 INFO: device_name: ap-41.off.lab
    19/05/2020 07:16:11 INFO: audit_id: b2b06f12-02f1-48d7-9682-f82766c4002c
    19/05/2020 07:16:11 INFO: org_id: 203d3d02-dbc0-4c1b-9f41-76896a3330f4
    19/05/2020 07:16:11 INFO: site_id: fa018c13-008b-46ae-aa18-1eeb894a96c4
    19/05/2020 07:16:11 INFO: site_name: lab
    19/05/2020 07:16:11 INFO: timestamp: 1589872563
    19/05/2020 07:16:11 INFO: type: AP_CONFIGURED
        '''
        self.text = f"{self.device_text} \"{self.device_name}\" (MAC: {self.device_mac})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""
        self.text += f" is now {self.event_type.split('_')[1]}"

    def _disconnected_long(self):
        '''
    19/05/2020 07:16:11 INFO: device-events
    19/05/2020 07:16:11 INFO: ap: d420b0002e95
    19/05/2020 07:16:11 INFO: device_name: ap-41.off.lab
    19/05/2020 07:16:11 INFO: audit_id: b2b06f12-02f1-48d7-9682-f82766c4002c
    19/05/2020 07:16:11 INFO: org_id: 203d3d02-dbc0-4c1b-9f41-76896a3330f4
    19/05/2020 07:16:11 INFO: site_id: fa018c13-008b-46ae-aa18-1eeb894a96c4
    19/05/2020 07:16:11 INFO: site_name: lab
    19/05/2020 07:16:11 INFO: timestamp: 1589872563
    19/05/2020 07:16:11 INFO: type: AP_CONFIGURED
        '''
        self.text = f"{self.device_text} \"{self.device_name}\" (MAC: {self.device_mac})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""
        self.text += " is DISCONNECTED FOR A LONG TIME"

    def _restarted(self):
        '''
    19/05/2020 07:16:11 INFO: device-events
    19/05/2020 07:16:11 INFO: ap: d420b0002e95
    19/05/2020 07:16:11 INFO: device_name: ap-41.off.lab
    19/05/2020 07:16:11 INFO: audit_id: b2b06f12-02f1-48d7-9682-f82766c4002c
    19/05/2020 07:16:11 INFO: org_id: 203d3d02-dbc0-4c1b-9f41-76896a3330f4
    19/05/2020 07:16:11 INFO: site_id: fa018c13-008b-46ae-aa18-1eeb894a96c4
    19/05/2020 07:16:11 INFO: site_name: lab
    19/05/2020 07:16:11 INFO: timestamp: 1589872563
    19/05/2020 07:16:11 INFO: type: AP_CONFIGURED
        '''
        self.text = f"{self.device_text} \"{self.device_name}\" (MAC: {self.device_mac})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""
        self.text += " RESTARTED"

    def _restarted_by_user(self):
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
        self.text = f"{self.device_text} \"{self.device_name}\" (MAC: {self.device_mac})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""
        self.text += "has been RESTARTED BY A USER"

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
        self.text = f"FIRMWARE UPGRADE FINISHED for the {self.device_text} \"{self.device_name}\" (MAC: {self.device_name})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""

    def _upgrade_failed(self):
        '''
{
    "type": "AP_UPGRADE_FAILED",
    "timestamp": 1552408871,
    "org_id": "2818e386-8dec-2562-9ede-5b8a0fbbdc71",
    "site_id": "4ac1dcf4-9d8b-7211-65c4-057819f0862b",
    "ap": "5c5b35000001",
    "audit_id": "e9a88814-fa81-5bdc-34b0-84e8735420e5"
}
        '''
        self.text = f"FIRMWARE UPGRADE FAILED for the {self.device_text} \"{self.device_name}\" (MAC: {self.device_name})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""

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
        self.text = f"FIRMWARE UPGRADE REQUESTED for the {self.device_text} \"{self.device_name}\" (MAC: {self.device_name})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""

    def _config_changed_by_user(self):
        '''
{
    "type": "AP_CONFIG_CHANGED_BY_USER",
    "timestamp": 1552408871,
    "org_id": "2818e386-8dec-2562-9ede-5b8a0fbbdc71",
    "site_id": "4ac1dcf4-9d8b-7211-65c4-057819f0862b",
    "ap": "5c5b35000001",
    "audit_id": "e9a88814-fa81-5bdc-34b0-84e8735420e5"
}
        '''
        self.text = f"CONFIGURATION CHANGED for the {self.device_text} \"{self.device_name}\" (MAC: {self.device_name})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""

    def _configured(self):
        '''
    19/05/2020 07:16:11 INFO: device-events
    19/05/2020 07:16:11 INFO: ap: d420b0002e95
    19/05/2020 07:16:11 INFO: device_name: ap-41.off.lab
    19/05/2020 07:16:11 INFO: audit_id: b2b06f12-02f1-48d7-9682-f82766c4002c
    19/05/2020 07:16:11 INFO: org_id: 203d3d02-dbc0-4c1b-9f41-76896a3330f4
    19/05/2020 07:16:11 INFO: site_id: fa018c13-008b-46ae-aa18-1eeb894a96c4
    19/05/2020 07:16:11 INFO: site_name: lab
    19/05/2020 07:16:11 INFO: timestamp: 1589872563
    19/05/2020 07:16:11 INFO: type: AP_CONFIGURED
        '''
        self.text = f"{self.device_text} \"{self.device_name}\" (MAC: {self.device_mac})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""
        self.text += f" has been {self.event_type.split('_')[1]}"

    def _cert_regenerated(self):
        '''
{
    "type": "AP_CERT_REGENERATED",
    "timestamp": 1552408871,
    "org_id": "2818e386-8dec-2562-9ede-5b8a0fbbdc71",
    "site_id": "4ac1dcf4-9d8b-7211-65c4-057819f0862b",
    "ap": "5c5b35000001"
}
        '''
        self.text = f"CERTIFICATE REGENERATED the for {self.device_text} \"{self.device_name}\" (MAC: {self.device_name})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""

    def _config_failed(self):
        '''
{
    "site_id": "f5fcbee5-fbca-45b3-8bf1-1619ede87879",
    "device_name": "sw-jn-01a",
    "timestamp": 1638456741,
    "device_type": "switch",
    "org_id": "203d3d02-dbc0-4c1b-9f41-76896a3330f4",
    "type": "SW_CONFIG_FAILED",
    "site_name": "PLE",
    "mac": "2c21311c37b0",
    "text": "error commit-confirm: [edit] apply-groups g1: mgd: Configuration group 'g1' is not defined"
}
        '''
        self.text = f"CONFIG FAILED for {self.device_text} \"{self.device_name}\" (MAC: {self.device_name})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""

#### SW and GW
    def _port(self):
        '''
{
    "device_name": "SSR-SPOKE-01",
    "site_name": "BR-Spoke-01",
    "type": "GW_PORT_UP",
    "text": "up on interface dh00000004",
    "org_id": "203d3d02-dbc0-4c1b-9f41-76896a3330f4",
    "device_type": "gateway",
    "site_id": "f5fcbee5-fbca-45b3-8bf1-1619ede87879",
    "mac": "020001bdfb60",
    "timestamp": 1646673351
}
        '''
        try:
            port = self.event["text"].split("ifName ")[1]
        except:
            port = "unknown"
        self.text = f"INTERFACE \"{port}\" on {self.device_text} \"{self.device_name}\" (MAC: {self.device_name})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""
        tmp = self.event_type.split("_")
        self.text += f" is {tmp[len(tmp)-1]}"

    def _ospf(self):
        '''
{
    "timestamp": 1613427890,
    "org_id": "b4e16c72-d50e-4c03-a952-a3217e231e2c",
    "site_id": "00000000-0000-0000-0000-000000000000",
    "type": "SW_OSPF_NEIGHBOR_UP",
    "device_type": "switch",
    "text": "RPD_OSPF_NBRUP: OSPF neighbor 255.255.255.10 (realm ospf-v2 xe-1/2/2.0 area 0.0.0.0) state changed from Init to ExStart due to 2WayRcvd (event reason: neighbor detected this router)",
    "mac": "20d80b062d00"
}
        '''
        self.text = f"OSPF NEIGHBOR for the {self.device_text} \"{self.device_name}\" (MAC: {self.device_name})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""
        tmp = self.event_type.split("_")
        self.text += f"is {tmp[len(tmp)-1]}"

    def _bgp(self):
        '''
{
    "timestamp": 1599046353,
    "org_id": "b4e16c72-d50e-4c03-a952-a3217e231e2c",
    "site_id": "2102aa05-b1ae-4d2d-88dc-c1bf9d834b9e",
    "type": "GW_BGP_NEIGHBOR_STATE_CHANGED",
    "model": "SRX300",
    "device_type": "gateway",
    "text": "RPD_BGP_NEIGHBOR_STATE_CHANGED: BGP peer 192.168.4.1 (Internal AS 65000) changed state from OpenConfirm to Established (event RecvKeepAlive) (instance master)",
    "version": "20.2R1.6",
    "mac": "f4cc552aba80"
}
        '''
        self.text = f"State of the BGP NEIGHBOR CHANGED for the {self.device_text} \"{self.device_name}\" (MAC: {self.device_name})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""
        self.text += "."

    def _ztp(self):
        '''
{
    "type": "SW_ZTP_FINISHED",
    "site_id": "f688779c-e335-4f88-8d7c-9c5e9964528b",
    "org_id": "b4e16c72-d50e-4c03-a952-a3217e231e2c",
    "mac": "1c9c8cba2e7f",
    "version": "18.2R3.4"
}
        '''
        self.text = f"ZTP PROCESS for the {self.device_text} with MAC Address {self.device_name}"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""
        self.text += " is FINISHED"

    def _config_lock_failed(self):
        '''
{
    "org_id": "c080ce4d-4e35-4373-bdc4-08df15d257f5",
    "site_id": "1df889ad-9111-4c0e-a00b-8a008b83eb68",
    "type": "GW_CONFIG_LOCK_FAILED",
    "text": "error lock-configuration: Error invoking '<lock-configuration/>': Netconf-Disconnected during <lock-configuration/> after 0ms, tx=21B , reply: <nil>",
    "model": "SRX320-POE",
    "version": "20.2R1-S2.1",
    "mac": "1c9c8cba2e7f"
}
        '''
        self.text = f"CONFIGURATION on {self.device_text} \"{self.device_name}\" (MAC: {self.device_name})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""
        self.text += " is LOCKED"

    def _alarm(self):
        '''
{
    "site_name": "BR-Spoke-01",
    "site_id": "f5fcbee5-fbca-45b3-8bf1-1619ede87879",
    "type": "GW_ALARM",
    "timestamp": 1647561800,
    "device_type": "gateway",
    "device_name": "ro-jn-01",
    "mac": "9ccc83b1f480",
    "org_id": "203d3d02-dbc0-4c1b-9f41-76896a3330f4",
    "text": "License for feature av_key_sophos_engine(69) is about to expire"
}
        '''
        self.text = f"ALARM for {self.device_text} \"{self.device_name}\" (MAC: {self.device_name})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""
        if self.event_text:
            self.text += f": \"{self.event_text}\""

    def _upgrade_pending(self):
        '''
{
    "key": "SW_UPGRADE_PENDING",
    "display": "Upgrade Pending",
    "description": "Switch upgrade pending restart",
    f"example": {
        "org_id": "a751df9c-897b-4065-9f34-d784c083dd0d",
        "site_id": "819b44b2-42ef-459d-8e59-29c5577b2330",
        "type": "SW_UPGRADE_PENDING",
        "text": "from version 19.1 to 19.3",
        "mac": "1c9c8cba2e7f"
    }
}
        '''
        self.text = f"UPGRADE for the {self.device_text} \"{self.device_name}\" (MAC: {self.device_name})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""
        self.text += f" {self.event_text} is PENDING."

    def _service_restart(self):
        '''
{
    "org_id": "c080ce4d-4e35-4373-bdc4-08df15d257f5",
    "site_id": "1df889ad-9111-4c0e-a00b-8a008b83eb68",
    "type": "SW_SYSTEM_SERVICE_RESTART",
    "text": "Unlock config DB due to it has been locked too long",
    "model": "EX4300-48MP",
    "version": "20.2R3.9",
    "mac": "1c9c8cba2e7f"
}
        '''
        self.text = f"SERVICE RESTARTED on the {self.device_text} \"{self.device_name}\" (MAC: {self.device_name})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""
        self.text += f" with error \"{self.event_text}\""

    def _arp(self):
        '''
{
    "org_id": "c080ce4d-4e35-4373-bdc4-08df15d257f5",
    "site_id": "1df889ad-9111-4c0e-a00b-8a008b83eb68",
    "type": "GW_ARP_RESOLVED",
    "mac": "0c8126c6ff6c",
    "model": "SSR"
}
        '''
        self.text = f"Gateway ARP for the {self.device_text} \"{self.device_name}\" (MAC: {self.device_name})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""
        tmp = self.event_type.split("_")
        self.text += f"is {tmp[len(tmp)-1]}"

    def _dhcp(self):
        '''
{
    "org_id": "c080ce4d-4e35-4373-bdc4-08df15d257f5",
    "site_id": "1df889ad-9111-4c0e-a00b-8a008b83eb68",
    "type": "GW_DHCP_RESOLVED",
    "mac": "0c8126c6ff6c",
    "model": "SSR"
}
        '''
        self.text = f"DHCP for the {self.device_text} \"{self.device_name}\" (MAC: {self.device_name})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""
        tmp = self.event_type.split("_")
        self.text += f"is {tmp[len(tmp)-1]}"

    def _rejected(self):
        '''
{
    "timestamp": 1613427890,
    "org_id": "b4e16c72-d50e-4c03-a952-a3217e231e2c",
    "site_id": "00000000-0000-0000-0000-000000000000",
    "type": "GW_REJECTED",
    "device_type": "unknown",
    "text": "ERROR: Unable to create ssh client: ssh: handshake failed: ssh: unable to authenticate, attempted methods [none password], no supported methods remain",
    "mac": "20d80b062d00"
}
        '''
        self.text = f"{self.device_text} \"{self.device_name}\" (MAC: {self.device_mac})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""
        self.text += "has been REJECTED"
