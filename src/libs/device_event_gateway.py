from .device_event_common import CommonEvent

class GatewayEvent(CommonEvent):

    def __init__(self, mist_host, message_levels, event):
        CommonEvent.__init__(self, mist_host, message_levels, event)



    def process(self):
        if self.event_type in ["GW_CLAIMED", "GW_UNCLAIMED"]:
            self._claimed()
        elif self.event_type == "GW_ASSIGNED":
            self._assigned()
        elif self.event_type == "GW_UNASSIGNED":
            self._unassigned()
        elif self.event_type == "GW_ZTP_FINISHED":
            self._ztp()
        elif self.event_type == "GW_CONFIG_CHANGED_BY_USER":
            self._config_changed_by_user()
        elif self.event_type in ["GW_CONFIGURED", "GW_RECONFIGURED"]:
            self._configured()
        elif self.event_type == "GW_CONFIG_LOCK_FAILED":
            self._config_lock_failed()
        elif self.event_type == "GW_CONFIG_FAILED":
            self._config_failed()
        if self.event_type in ["GW_PORT_DOWN", "GW_PORT_UP"]:
            self._port()
        elif self.event_type in ["GW_CONNECTED", "GW_DISCONNECTED"]:
            self._connected()
        elif self.event_type =="GW_RESTARTED":
            self._restarted()
        elif self.event_type =="GW_RESTARTED_BY_USER":
            self._restarted_by_user()
        elif self.event_type == "GW_DISCONNECTED_LONG":
            self._disconnected_long()
        elif self.event_type in ["GW_OSPF_NEIGHBOR_UP", "GW_OSPF_NEIGHBOR_DOWN"]:
            self._ospf()
        elif self.event_type == "GW_BGP_NEIGHBOR_STATE_CHANGED":
            self._bgp()
        elif self.event_type in ["GW_VPN_PEER_UP", "GW_VPN_PEER_DOWN"]:
            self._gw_vpn_peer()
        elif self.event_type in ["GW_VPN_PATH_UP", "GW_VPN_PATH_DOWN"]:
            self._gw_vpn_path()
        elif self.event_type == "GW_CERT_REGENERATED":
            self._cert_regenerated()
        elif self.event_type == "GW_ALARM":
            self._alarm()
        elif self.event_type == "GW_UPGRADE_BY_USER":
            self._upgrade_by_user()
        elif self.event_type == "GW_UPGRADED":
            self._upgraded()
        elif self.event_type == "GW_UPGRADE_PENDING":
            self._upgrade_pending()
        elif self.event_type == "GW_UPGRADE_FAILED":
            self._upgrade_failed()
        elif self.event_type == "GW_SYSTEM_SERVICE_RESTART":
            self._service_restart()
        elif self.event_type in ["GW_CONDUCTOR_DISCONNECTED", "GW_CONDUCTOR_CONNECTED"]:
            self._gw_conductor()
        elif self.event_type in ["GW_ARP_RESOLVED", "GW_ARP_UNRESOLVED"]:
            self._arp()
        elif self.event_type in ["GW_DHCP_RESOLVED", "GW_DHCP_UNRESOLVED"]:
            self._dhcp()
        elif self.event_type in ["GW_HA_CONTROL_LINK_UP", "GW_HA_CONTROL_LINK_DOWN"]:
            self._gw_ha_link()
        elif self.event_type in ["GW_HA_HEALTH_WEIGHT_LOW", "GW_HA_HEALTH_WEIGHT_RECOVERY"]:
            self._gw_ha_health()
        elif self.event_type == "GW_REJECTED":
            self._rejected()
        elif self.event_type == "GW_RG_STATE_CHANGED":
            self._gw_rg_state()
        elif self.event_type == "GW_PORT_RG_STATE_CHANGED":
            self._gw_port_rg_state()
        else:
            self._common()


    def _gw_vpn_peer(self):
        '''
{
    "timestamp": 1598371008,
    "org_id": "b4e16c72-d50e-4c03-a952-a3217e231e2c",
    "site_id": "2102aa05-b1ae-4d2d-88dc-c1bf9d834b9e",
    "type": "GW_VPN_PEER_DOWN",
    "model": "SRX300",
    "device_type": "gateway",
    "text": "TODO",
    "version": "20.2R1.6",
    "mac": "f4cc552aba80"
}
        '''
        self.text = f"VPN PEER for Gateway \"{self.device_name}\" (MAC: {self.device_mac})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""
        tmp = self.event_type.split("_")
        self.text += f"is {tmp[len(tmp)-1]}"


    def _gw_vpn_path(self):
        '''
{
    "site_name": "BR-Spoke-02",
    "site_id": "d6cb89ee-5b51-47ff-9e17-7bee23476d0f",
    "type": "GW_VPN_PATH_DOWN",
    "timestamp": 1647507731,
    "device_type": "gateway",
    "device_name": "SSR-SPOKE-02",
    "mac": "0200015b6fd7",
    "org_id": "203d3d02-dbc0-4c1b-9f41-76896a3330f4",
    "text": "peer path [SSR-HUB-01,10.3.128.34,SSR-SPOKE-02-A,ADSL,0] down"
}
        '''
        self.text = f"VPN PATH for Gateway \"{self.device_name}\" (MAC: {self.device_mac})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""
        tmp = self.event_type.split("_")
        self.text += f"is {tmp[len(tmp)-1]}"

    def _gw_conductor(self):
        '''
{
    "org_id": "c080ce4d-4e35-4373-bdc4-08df15d257f5",
    "site_id": "1df889ad-9111-4c0e-a00b-8a008b83eb68",
    "type": "GW_CONDUCTOR_DISCONNECTED",
    "mac": "0c8126c6ff6c",
    "model": "SSR"
}
        '''
        self.text = f"Gateway \"{self.device_name}\" (MAC: {self.device_mac})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""
        tmp = self.event_type.split("_")
        self.text += f"is {tmp[len(tmp)-1]}"
        self.text += " from the Conductor"

    def _gw_ha_link(self):
        '''
{
    "org_id": "c080ce4d-4e35-4373-bdc4-08df15d257f5",
    "site_id": "1df889ad-9111-4c0e-a00b-8a008b83eb68",
    "type": "GW_HA_CONTROL_LINK_UP",
    "mac": "0c8126c6ff6c",
    "device_type": "gateway",
    "text": "JSRPD_HA_CONTROL_LINK_UP: HA control link monitor status is marked up",
    "model": "SSR"
}
        '''
        self.text = f"HA CONTROL LINK for the Gateway \"{self.device_name}\" (MAC: {self.device_mac})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""
        tmp = self.event_type.split("_")
        self.text += f"is {tmp[len(tmp)-1]}"

    def _gw_ha_health(self):
        '''
{
    "org_id": "c080ce4d-4e35-4373-bdc4-08df15d257f5",
    "site_id": "1df889ad-9111-4c0e-a00b-8a008b83eb68",
    "type": "GW_HA_HEALTH_WEIGHT_LOW",
    "mac": "0c8126c6ff6c",
    "device_type": "gateway",
    "text": "JSRPD_HA_HEALTH_WEIGHT_LOW: Detected cluster1-Node0-RG1's health weight(0) low, send out SNMP trap",
    "model": "SRX345"
}
        '''
        self.text = f"HA HEALTH for the Gateway \"{self.device_name}\" (MAC: {self.device_mac})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""
        tmp = self.event_type.split("_")
        self.text += f"is {tmp[len(tmp)-1]}"

    def _gw_rg_state(self):
        '''
{
    "timestamp": 1613427890,
    "org_id": "b4e16c72-d50e-4c03-a952-a3217e231e2c",
    "site_id": "00000000-0000-0000-0000-000000000000",
    "type": "GW_RG_STATE_CHANGED",
    "device_type": "gateway",
    "text": "JSRPD_RG_STATE_CHANGE: Redundancy-group 1 transitioned from 'secondary-hold' to 'secondary' state due to Ready to become secondary",
    "mac": "20d80b062d00"
}
        '''
        self.text = f"REDUNDANCY GROUP STATE CHANGED for the Gateway \"{self.device_name}\" (MAC: {self.device_mac})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""

    def _gw_port_rg_state(self):
        '''
{
    "org_id": "c080ce4d-4e35-4373-bdc4-08df15d257f5",
    "site_id": "1df889ad-9111-4c0e-a00b-8a008b83eb68",
    "type": "GW_PORT_RG_STATE_CHANGED",
    "mac": "0c8126c6ff6c",
    "device_type": "gateway",
    "text": "Gateway port RG state was changed to active/standby",
    "model": "SSR",
    "node": "node0",
    "port_id": "dpdk2",
    "timestamp": 1613427890
}
        '''
        self.text = f"PORT REDUNDANCY GROUP STATE CHANGED for the Gateway \"{self.device_name}\" (MAC: {self.device_mac})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""
