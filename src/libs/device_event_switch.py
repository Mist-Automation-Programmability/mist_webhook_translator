from datetime import datetime, timedelta
from .device_event_common import CommonEvent


class SwitchEvent(CommonEvent):

    def __init__(self, mist_host, message_levels, event):
        CommonEvent.__init__(self, mist_host, message_levels, event)


    def _process(self):
        if self.event_type in ["SW_PORT_DOWN", "SW_PORT_UP"]:
            self._sw_port()
        elif self.event_type == "SW_CONFIG_CHANGED_BY_USER":
            self._config_changed_by_user()
        elif self.event_type in ["SW_CONFIGURED", "SW_CONFIG_CHANGED_BY_USER", "SW_RECONFIGURED", "SW_RESTARTED", "SW_RESTART_BY_USER", "SW_CONNECTED", "SW_DISCONNECTED", "SW_DISCONNECTED_LONG"]:
            self._common()
        elif self.event_type == "SW_DYNAMIC_PORT_ASSIGNED":
            self._sw_dynamic_port()
        elif self.event_type == "SW_CONFIG_FAILED":
            self._sw_config_failed()
        elif self.event_type == "SW_ASSIGNED":
            self._assigned()
        elif self.event_type == "SW_UNASSIGNED":
            self._unassigned()
        elif self.event_type == "SW_UPGRADE_BY_USER":
            self._upgrade_by_user()
        elif self.event_type == "SW_UPGRADED":
            self._upgraded()
        elif self.event_type == "SW_UNCLAIMED":
            self._unclaimed()
        elif self.event_type == "SW_CLAIMED":
            self._claimed()
        else:
            self.text.append("Switch Name: %s" % (self.device_name))
            self.text.append("Switch MAC: %s" % (self.device_mac))
            self.text.append("Site: %s" % (self.site_name))
            self.text.append("Event: %s" % (self.event_type))
            self.text.append("Reason: %s" % (self.reason))
            
        
    def _sw_port(self):        
        '''
    28/09/2020 06:35:31 INFO: device-events
    28/09/2020 06:35:31 INFO: device_name: sw-jn-01
    28/09/2020 06:35:31 INFO: device_type: switch
    28/09/2020 06:35:31 INFO: mac: 2c21311c37b0
    28/09/2020 06:35:31 INFO: org_id: 203d3d02-dbc0-4c1b-9f41-76896a3330f4
    28/09/2020 06:35:31 INFO: site_id: f5fcbee5-fbca-45b3-8bf1-1619ede87879
    28/09/2020 06:35:31 INFO: site_name: lab
    28/09/2020 06:35:31 INFO: text: SNMP_TRAP_LINK_DOWN: ifIndex 518, ifAdminStatus up(1), ifOperStatus down(2), ifName ge-0/0/4
    28/09/2020 06:35:31 INFO: timestamp: 1601274808
    28/09/2020 06:35:31 INFO: type: SW_PORT_DOWN
        '''
        port = "unknown"
        for tpart in self.event["text"].split(","):
            if "ifName" in tpart:
                port = tpart.replace("ifName","").replace(" ","")
        text_string = "Port \"{0}\" on switch \"{1}\" (MAC: {2}) ".format(port, self.device_name, self.device_mac)
        if self.site_name:
            text_string += "on site \"{0}\" ".format(self.site_name)
        text_string += "is {0}.".format(self.event_type.replace("SW_PORT_", "").title())
        self.text.append(text_string)
        
    def _sw_dynamic_port(self):        
        '''
    23/10/2020 08:02:26 INFO: device-events
    23/10/2020 08:02:26 INFO: device_name: sw-jn-01
    23/10/2020 08:02:26 INFO: device_type: switch
    23/10/2020 08:02:26 INFO: mac: 2c21311c37b0
    23/10/2020 08:02:26 INFO: org_id: 203d3d02-dbc0-4c1b-9f41-76896a3330f4
    23/10/2020 08:02:26 INFO: site_id: f5fcbee5-fbca-45b3-8bf1-1619ede87879
    23/10/2020 08:02:26 INFO: site_name: lab
    23/10/2020 08:02:26 INFO: text: Interface ge-0/0/0 is assigned to port profile: lab_reg
    23/10/2020 08:02:26 INFO: timestamp: 1603439910
    23/10/2020 08:02:26 INFO: type: SW_DYNAMIC_PORT_ASSIGNED
        '''
        text_string = "Dynamic Port Assignment on switch \"{0}\" (MAC: {1}) ".format(self.device_name, self.device_mac)        
        if self.site_name:
            text_string += "on site \"{0}\" ".format(self.site_name)
        text_string += ". {0}".format(self.event["text"])
        self.text.append(text_string)


    def _sw_config_failed(self):        
        '''
21/11/2020 01:44:44 INFO: device-events
21/11/2020 01:44:44 INFO: device_name: ro-jn-01
21/11/2020 01:44:44 INFO: device_type: gateway
21/11/2020 01:44:44 INFO: mac: 9ccc83b1f480
21/11/2020 01:44:44 INFO: org_id: 203d3d02-dbc0-4c1b-9f41-76896a3330f4
21/11/2020 01:44:44 INFO: site_id: f5fcbee5-fbca-45b3-8bf1-1619ede87879
21/11/2020 01:44:44 INFO: site_name: lab
21/11/2020 01:44:44 INFO: text: error commit-confirm: Error invoking '<commit-configuration><log>version=1605036925</log><confirmed/><confirm-timeout>10</confirm-timeout></commit-configuration>': Netconf-ExecTimeout <nil>
21/11/2020 01:44:44 INFO: timestamp: 1605923075
21/11/2020 01:44:44 INFO: type: GW_CONFIG_FAILED
        '''
        text_string = "Config failed on switch \"{0}\" (MAC: {1}) ".format(self.device_name, self.device_mac)
        if self.site_name:
            text_string += "on site \"{0}\" ".format(self.site_name)
        text_string += "with error \"{0}\".".format(self.event_text.split(":")[1])        
        self.text.append(text_string)
       