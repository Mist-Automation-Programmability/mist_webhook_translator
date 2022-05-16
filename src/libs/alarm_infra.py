from datetime import datetime, timedelta
from .alarm_common import CommonAlarm


class InfraAlarm(CommonAlarm):

    def __init__(self, mist_host, alarm_channels, event):
        self.model = event.get("model", None)
        self.fw_version = event.get("fw_version", None)
        self.port_ids = event.get("port_ids", None)
        self.servers = event.get("servers", [])
        self.ssids = event.get("ssids", [])
        self.vlans = event.get("vlans", [])
        if "reason" in event:
            self.reason = event.get("reason")
        elif "reasons" in event:
            self.reason = event.get("reasons")
        else:
            self.reason = None
        CommonAlarm.__init__(self, mist_host, alarm_channels, event)

    def _process(self):
        if self.alarm_type in [
            "device_down", "switch_down", "gateway_down",
            "device_restarted", "switch_restarted",
            "device_reconnected", "switch_reconnected", "gateway_reconnected",
            "vpn_peer_down",
            "vc_master_changed", "vc_backup_failed", "vc_member_added", "vc_member_deleted",
            "sw_alarm_chassis_poe", "sw_alarm_chassis_pem", "sw_alarm_chassis_psu", "sw_alarm_chassis_partition",
            "sw_bgp_neighbor_state_changed", "sw_bad_optics", "sw_bpdu_error"
            "sw_dhcp_pool_exhausted", "gw_dhcp_pool_exhausted",
        ]:
            self._infra()
        else:
            self._common()

    def _infra(self):
        '''
        '''
        self.text = f"{self.alarm_type.replace('_', ' ').upper()} detected on site {self.site_name}"
        if self.hostnames:
            self.info.append(
                f"*HOSTNAMES*: {', '.join(self.hostnames)}")
        if self.aps:
            self.info.append(f"*APs*: {', '.join(self.aps)}")
        if self.switches:
            self.info.append(
                f"*SWITCHES*: {', '.join(self.switches)}")
        if self.gateways:
            self.info.append(
                f"*GATEWAYS*: {', '.join(self.gateways)}")
        if self.port_ids:
            self.info.append(
                f"*PORT IDS*: {', '.join(self.port_ids)}")
        if self.reason:
            self.info.append(
                f"*REASON*: {', '.join(self.reason)}")
        if self.servers:
            self.info.append(
                f"*SERVERS*: {', '.join(self.servers)}")
        if self.ssids:
            self.info.append(
                f"*SSIDS*: {', '.join(self.ssids)}")
        if self.vlans:
            self.info.append(
                f"*VLANS*: {', '.join(self.vlans)}")
