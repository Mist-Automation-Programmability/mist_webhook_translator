from .device_event_common import CommonEvent


class ApEvent(CommonEvent):

    def __init__(self, mist_host, message_levels, event):
        self.band = event.get("band", None)
        self.channel = event.get("channel", None)
        self.bandwidth = event.get("bandwidth", None)
        self.power = event.get("power", None)
        self.pre_channel = event.get("pre_channel", None)
        self.pre_bandwidth = event.get("pre_bandwidth", None)
        self.pre_power = event.get("pre_power", None)
        self.occurrence = event.get("occurrence", None)
        CommonEvent.__init__(self, mist_host, message_levels, event)


    def _process(self):
        if self.event_type in ["AP_CLAIMED", "AP_UNCLAIMED"]:
            self._claimed()
        elif self.event_type == "AP_ASSIGNED":
            self._assigned()
        elif self.event_type == "AP_UNASSIGNED":
            self._unassigned()
        elif self.event_type == "AP_CONFIG_CHANGED_BY_RRM":
            self._ap_config_changed_by_rrm()
        elif self.event_type == "AP_CONFIG_CHANGED_BY_USER":
            self._config_changed_by_user()
        elif self.event_type == "AP_CONFIG_FAILED":
            self._config_failed()
        elif self.event_type in ["AP_CONFIGURED", "AP_RECONFIGURED"]:
            self._configured()
        elif self.event_type == "1026":
            self._ap_event_1026()
        elif self.event_type == "AP_RRM_ACTION":
            self._ap_rrm_action()
        elif self.event_type == "AP_BEACON_STUCK":
            self._ap_beacon_stuck()
        elif self.event_type == "AP_RADAR_DETECTED":
            self._ap_radar_detected()
        elif self.event_type == "AP_RESTART_BY_USER":
            self._restarted_by_user()
        elif self.event_type in ["AP_CONNECTED", "AP_DISCONNECTED"]:
            self._connected()
        elif self.event_type =="AP_RESTARTED":
            self._restarted()
        elif self.event_type == "AP_DISCONNECTED_LONG":
            self._disconnected_long()
        elif self.event_type == "AP_UPGRADE_BY_USER":
            self._upgrade_by_user()
        elif self.event_type == "AP_UPGRADED":
            self._upgraded()
        elif self.event_type == "AP_UPGRADE_BY_SCHEDULE":
            self._ap_upgraded_by_schedule()
        elif self.event_type == "AP_UPGRADE_BY_USER":
            self._upgrade_by_user()
        elif self.event_type == "AP_UPGRADE_FAILED":
            self._upgrade_failed()
        elif self.event_type == "AP_CERT_REGENERATED":
            self._cert_regenerated()
        elif self.event_type == "AP_GET_SUPPORT_FILES":
            self._ap_support_file()
        else:
            self._common()


    def _ap_config_changed_by_rrm(self):
        '''
{
    "type": "AP_CONFIGURED",
    "timestamp": 1552408871,
    "org_id": "2818e386-8dec-2562-9ede-5b8a0fbbdc71",
    "site_id": "4ac1dcf4-9d8b-7211-65c4-057819f0862b",
    "ap": "5c5b35000001"
}
        '''
        self.text = f"Configuration for AP \"{self. device_name}\" (MAC: {self.device_mac})"
        if self.site_name:
            self.text +=  f" on site \"{self.site_name}\""
        self.text += " is changed by RRM."
        

    def _ap_event_1026(self):
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
        self.text = f"Event 1026 for AP \"{self. device_name}\" (MAC: {self.device_mac})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""

    def _ap_rrm_action(self):
        '''
{
    "type": "AP_RRM_ACTION",
    "timestamp": 1552408871,
    "org_id": "2818e386-8dec-2562-9ede-5b8a0fbbdc71",
    "site_id": "4ac1dcf4-9d8b-7211-65c4-057819f0862b",
    "ap": "5c5b35000001",
    "band": "5",
    "channel": 36,
    "bandwidth": 40,
    "power": 17,
    "pre_channel": 40,
    "pre_bandwidth": 40,
    "pre_power": 15,
    "audit_id": "e9a88814-fa81-5bdc-34b0-84e8735420e5",
    "reason": "radar-detected"
}
        '''
        self.text = f"RRM CHANGES in {self.band}GHz for the AP \"{self. device_name}\" (MAC: {self.device_mac})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""
        self.text += f"from channel {self.pre_channel}/{self.pre_bandwidth}MHz at {self.pre_power}dBm to {self.channel}/{self.bandwidth}MHz at {self.power}Dbm"

    def _ap_beacon_stuck(self):
        '''
{
    "type": "AP_BEACON_STUCK",
    "timestamp": 1552233041,
    "org_id": "2818e386-8dec-2562-9ede-5b8a0fbbdc71",
    "site_id": "4ac1dcf4-9d8b-7211-65c4-057819f0862b",
    "ap": "5c5b35000001",
    "band": "5",
    "start_time": 1552008073,
    "end_time": 1552232053,
    "occurrence": 747
}
        '''
        self.text = f"{self.occurrence} BEANCON STUCK in {self.band}GHz for the AP \"{self. device_name}\" (MAC: {self.device_mac})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""


    def _ap_radar_detected(self):
        '''
{
    "type": "AP_RADAR_DETECTED",
    "timestamp": 1552233041,
    "org_id": "2818e386-8dec-2562-9ede-5b8a0fbbdc71",
    "site_id": "4ac1dcf4-9d8b-7211-65c4-057819f0862b",
    "ap": "5c5b35000001",
    "band": "5",
    "channel": 36,
    "bandwidth": 40,
    "pre_channel": 125,
    "pre_bandwidth": 40,
    "reason": "radar-detected"
}
        '''
        self.text = f"RADAR DETECTED on channel {self.pre_channel}/{self.pre_bandwidth}MHz by the AP \"{self. device_name}\" (MAC: {self.device_mac})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""
        self.text += f". AP moved to channel {self.channel}/{ self.bandwidth}MHz"

    def _ap_upgraded_by_schedule(self):
        '''
{
    "type": "AP_UPGRADE_BY_SCHEDULE",
    "timestamp": 1552408871,
    "org_id": "2818e386-8dec-2562-9ede-5b8a0fbbdc71",
    "site_id": "4ac1dcf4-9d8b-7211-65c4-057819f0862b",
    "ap": "5c5b35000001"
}
        '''
        self.text = f"AP \"{self. device_name}\" (MAC: {self.device_mac})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""
        self.text += " is UPGRADED BY SCHEDULE POLICY"

    def _ap_support_file(self):
        '''
{
    "type": "AP_GET_SUPPORT_FILES",
    "timestamp": 1552233041,
    "org_id": "2818e386-8dec-2562-9ede-5b8a0fbbdc71",
    "site_id": "4ac1dcf4-9d8b-7211-65c4-057819f0862b",
    "ap": "5c5b35000001",
    "device_type": "ap"
}
        '''
        self.text = f"SUPPORT FILE RETRIEVED for AP \"{self. device_name}\" (MAC: {self.device_mac})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""
