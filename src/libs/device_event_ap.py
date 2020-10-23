from datetime import datetime, timedelta
from .device_event_common import CommonEvent


class ApEvent(CommonEvent):

    def __init__(self, mist_host, message_levels, event):
        CommonEvent.__init__(self, mist_host, message_levels, event)


    def _process(self):
        if self.event_type == "AP_CONFIG_CHANGED_BY_RRM":
            self._ap_config_changed_by_rrm()
        elif self.event_type == "AP_CONFIG_CHANGED_BY_USER":
            self._config_changed_by_user()
        elif self.event_type == "1026":
            self._1026()
        elif self.event_type in ["AP_CONFIGURED", "AP_RECONFIGURED", "AP_RESTARTED", "AP_RESTART_BY_USER", "AP_CONNECTED", "AP_DISCONNECTED", "AP_DISCONNECTED_LONG"]:
            self._common()
        elif self.event_type == "AP_ASSIGNED":
            self._assigned()
        elif self.event_type == "AP_UNASSIGNED":
            self._unassigned()
        elif self.event_type == "AP_UPGRADE_BY_USER":
            self._upgrade_by_user()
        elif self.event_type == "AP_UPGRADED":
            self._upgraded()
        elif self.event_type == "AP_UNCLAIMED":
            self._unclaimed()
        elif self.event_type == "AP_CLAIMED":
            self._claimed()

        else:
            self.text.append("AP Name: %s" % (self.device_name))
            self.text.append("AP MAC: %s" % (self.device_mac))
            self.text.append("Site: %s" % (self.site_name))
            self.text.append("Event: %s" % (self.event_type))
            self.text.append("Reason: %s" % (self.reason))


    def _ap_config_changed_by_rrm(self):
        '''
    20/05/2020 06:30:53 INFO: device-events
    20/05/2020 06:30:53 INFO: ap: d420b0002e95
    20/05/2020 06:30:53 INFO: device_name: ap-41.off.lab
    20/05/2020 06:30:53 INFO: audit_id: 6175746f-0000-0000-3157-000000000000
    20/05/2020 06:30:53 INFO: org_id: 203d3d02-dbc0-4c1b-9f41-76896a3330f4
    20/05/2020 06:30:53 INFO: site_id: fa018c13-008b-46ae-aa18-1eeb894a96c4
    20/05/2020 06:30:53 INFO: site_name: lab
    20/05/2020 06:30:53 INFO: timestamp: 1589956241
    20/05/2020 06:30:53 INFO: type: AP_CONFIG_CHANGED_BY_RRM
        '''
        text_string = "Configuration for AP \"%s\" (MAC: %s) " % (
           self. device_name, self.device_mac)
        if self.site_name:
            text_string += "on site \"%s\" " % (self.site_name)
        text_string += "is changed by RRM."
        self.text.append(text_string)
        

    def _1026(self):
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
        text_string = "Event 1026 for AP \"%s\" (MAC: %s) " % (self.device_name, self.device_mac)
        if self.site_name:
            text_string += "on site \"%s\" " % (self.site_name)
        text_string += "because of %s." % (self.reason)
        self.text.append(text_string)
        
