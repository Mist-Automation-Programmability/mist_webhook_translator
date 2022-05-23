from datetime import datetime, timedelta
from .device_event_common import CommonEvent


class SwitchEvent(CommonEvent):

    def __init__(self, mist_host, message_levels, event):
        self.vc_master_id = event.get("vc-master-id", None)
        self.vc_backup_id = event.get("vc-backup-id", None)
        CommonEvent.__init__(self, mist_host, message_levels, event)

    def _process(self):
        if self.event_type in ["SW_CLAIMED", "SW_UNCLAIMED"]:
            self._claimed()
        elif self.event_type == "SW_ASSIGNED":
            self._assigned()
        elif self.event_type == "SW_UNASSIGNED":
            self._unassigned()
        elif self.event_type == "SW_ZTP_FINISHED":
            self._ztp()
        elif self.event_type == "SW_CONFIG_CHANGED_BY_USER":
            self._config_changed_by_user()
        elif self.event_type in ["SW_CONFIGURED", "SW_RECONFIGURED"]:
            self._configured()
        elif self.event_type == "SW_CONFIG_LOCK_FAILED":
            self._config_lock_failed()
        elif self.event_type == "SW_CONFIG_FAILED":
            self._config_failed()
        elif self.event_type in ["SW_PORT_DOWN", "SW_PORT_UP"]:
            self._port()
        elif self.event_type in ["SW_CONNECTED", "SW_DISCONNECTED"]:
            self._connected()
        elif self.event_type == "SW_RESTARTED_BY_USER":
            self._restarted_by_user()
        elif self.event_type == "SW_RESTARTED":
            self._restarted()
        elif self.event_type in ["SW_OSPF_NEIGHBOR_UP", "SW_OSPF_NEIGHBOR_DOWN"]:
            self._ospf()
        elif self.event_type == "SW_BGP_NEIGHBOR_STATE_CHANGED":
            self._bgp()
        elif self.event_type == "SW_ALARM":
            self._alarm()
        elif self.event_type in ["SW_ALARM_CHASSIS_PARTITION", "SW_ALARM_CHASSIS_POE", "SW_ALARM_CHASSIS_PSU"]:
            self._sw_alarm()
        elif self.event_type == "SW_UPGRADE_BY_USER":
            self._upgrade_by_user()
        elif self.event_type == "SW_UPGRADED":
            self._upgraded()
        elif self.event_type == "SW_UPGRADE_PENDING":
            self._upgrade_pending()
        elif self.event_type == "SW_UPGRADE_FAILED":
            self._upgrade_failed()
        elif self.event_type == "SW_SYSTEM_SERVICE_RESTART":
            self._service_restart()
        elif self.event_type == "SW_REJECTED":
            self._alarm()
        elif self.event_type == "SW_DYNAMIC_PORT_ASSIGNED":
            self._sw_dynamic_port()
        elif self.event_type == "SW_PORT_BPDU_BLOCKED":
            self._sw_bpdu()
        elif self.event_type == "SW_PORT_STORM_CONTROL":
            self._sw_storm()
        elif self.event_type == "SW_HANDSHAKE_ERROR":
            self._sw_handshake()
        elif self.event_type == "SW_STP_TOPO_CHANGED":
            self._sw_stp()
        elif self.event_type == "SW_VC_BACKUP_ELECTED":
            self._sw_vc_elected()
        elif self.event_type == "SW_VC_MASTER_CHANGED":
            self._sw_vc_changed()
        elif self.event_type in ["SW_VC_MEMBER_ADDED", "SW_VC_MEMBER_DELETED"]:
            self._sw_vc_member()
        elif self.event_type == "SW_MASTER_ON_RECOVERY":
            self._sw_master_rec()
        elif self.event_type == "SW_MEMBER_ON_RECOVERY":
            self._sw_member_rec()
        elif self.event_type in [
            "SW_RECOVERY_SNAPSHOT_REQUESTED",
            "SW_RECOVERY_SNAPSHOT_SUCCEEDED",
            "SW_RECOVERY_SNAPSHOT_FAILED"
        ]:
            self._sw_snapshot()
        elif self.event_type == "SW_RECOVERY_SNAPSHOT_NOTNEEDED":
            self._sw_snapshot_notneeded()
        elif self.event_type == "SW_RECOVERY_SNAPSHOT_UNSUPPORTED":
            self._sw_snapshot_unsported()
        elif self.event_type == "SW_DOT1XD_USR_AUTHENTICATED":
            self._sw_dot1x_user()
        elif self.event_type == "SW_RADIUS_SERVER_UNREACHABLE":
            self._sw_radius_unreachable()
        else:
            self._common()

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
        self.text = f"Dynamic Port Assignment on the Switch \"{self.device_name}\" (MAC: {self.device_mac})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""

    def _sw_alarm(self):
        '''
{
    "type": "SW_ALARM_CHASSIS_PARTITION",
    "site_id": "f688779c-e335-4f88-8d7c-9c5e9964528b",
    "org_id": "b4e16c72-d50e-4c03-a952-a3217e231e2c",
    "mac": "1c9c8cba2e7f",
    "alarm_class": "Minor",
    "text": "RE 0 /var partition usage is high",
    "version": "18.2R3.4"
}
        '''
        self.text = f"{self.event_type.replace('SW_ALARM_', '').replace('_', ' ')} ALARM for the Switch \"{self.device_name}\" (MAC: {self.device_mac})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""

    def _sw_bpdu(self):
        '''
{
    "timestamp": 1613427890,
    "org_id": "b4e16c72-d50e-4c03-a952-a3217e231e2c",
    "site_id": "00000000-0000-0000-0000-000000000000",
    "type": "SW_PORT_BPDU_BLOCKED",
    "device_type": "switch",
    "text": "L2CPD_RECEIVE_BPDU_BLOCK_ENABLED: BPDU_PROTECT: Interface ge-0/0/6 is DOWN: BPDU error detected",
    "mac": "20d80b062d00"
}
        '''
        self.text = f"PORT BPDU BLOCKED on the Switch \"{self.device_name}\" (MAC: {self.device_mac})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""

    def _sw_storm(self):
        '''
{
    "type": "SW_PORT_STORM_CONTROL",
    "timestamp": 1575922629,
    "site_id": "f688779c-e335-4f88-8d7c-9c5e9964528b",
    "org_id": "b4e16c72-d50e-4c03-a952-a3217e231e2c",
    "mac": "1c9c8cba2e7f",
    "version": "18.2R3.4",
    "text": "L2ALD_ST_CTL_IN_EFFECT: ge-0/0/1.0: storm control in effect on the port",
    "model": "EX2300-C-12P",
    "port_id": "ge-0/0/1"
}
        '''
        self.text = f"STORM CONTROL IN EFFECT on the Switch \"{self.device_name}\" (MAC: {self.device_mac})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""

    def _sw_handshake(self):
        '''
{
    "timestamp": 1613427890,
    "org_id": "b4e16c72-d50e-4c03-a952-a3217e231e2c",
    "site_id": "00000000-0000-0000-0000-000000000000",
    "type": "SW_HANDSHAKE_ERROR",
    "device_type": "unknown",
    "text": "ERROR: Unable to create ssh client: ssh: handshake failed: ssh: unable to authenticate, attempted methods [none password], no supported methods remain",
    "mac": "20d80b062d00"
}
        '''
        self.text = f"SWITCH HANDSHAKE ERROR on the Switch \"{self.device_name}\" (MAC: {self.device_mac})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""

    def _sw_stp(self):
        '''
{
    "org_id": "c080ce4d-4e35-4373-bdc4-08df15d257f5",
    "site_id": "1df889ad-9111-4c0e-a00b-8a008b83eb68",
    "type": "SW_STP_TOPO_CHANGED",
    "text": "TopoChgCnt 55, RootID 4096.d4:04:ff:9c:f1:a0, RootCost 2000, RootPort ae0",
    "model": "EX4300-48MP",
    "version": "20.2R3.9",
    "mac": "1c9c8cba2e7f"
}
        '''
        self.text = f"STP TOPOLOGY CHANGED on the Switch \"{self.device_name}\" (MAC: {self.device_mac})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""

    def _sw_vc_elected(self):
        '''
{
    "type": "SW_VC_BACKUP_ELECTED",
    "site_id": "f688779c-e335-4f88-8d7c-9c5e9964528b",
    "org_id": "b4e16c72-d50e-4c03-a952-a3217e231e2c",
    "mac": "1c9c8cba2e7f",
    "version": "18.2R3.4",
    "text": "CHASSISD_VCHASSIS_MEMBER_UPDATE_NOTICE: Membership update: Member 1->1, Mode Master->Master, 1M 0B, Master Unchanged, Members Changed",
    "vc-backup-id": 0
}
        '''
        self.text = f"The Switch \"{self.device_name}\" (MAC: {self.device_mac})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""
        self.text = f" has been elected as VC BACKUPED (member {self.vc_backup_id})"

    def _sw_vc_changed(self):
        '''
{
    "type": "SW_VC_MASTER_CHANGED",
    "site_id": "f688779c-e335-4f88-8d7c-9c5e9964528b",
    "org_id": "b4e16c72-d50e-4c03-a952-a3217e231e2c",
    "mac": "1c9c8cba2e7f",
    "version": "18.2R3.4",
    "text": "CHASSISD_VCHASSIS_MEMBER_UPDATE_NOTICE: Membership update: Member 1->1, Mode Backup->Master, 1M 2B, Master Changed, Members Changed",
    "vc-master-id": 1,
    "vc-backup-id": 2
}
        '''
        self.text = f"MASTER CHANGED on the Virtual Chassis \"{self.device_name}\" (MAC: {self.device_mac})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""
        self.text += f" from member {self.vc_backup_id} to member {self.vc_master_id}"

    def _sw_vc_member(self):
        '''
{
    "type": "SW_VC_MEMBER_ADDED",
    "site_id": "f688779c-e335-4f88-8d7c-9c5e9964528b",
    "org_id": "b4e16c72-d50e-4c03-a952-a3217e231e2c",
    "mac": "1c9c8cba2e7f",
    "version": "18.2R3.4",
    "text": "CHASSISD_VCHASSIS_MEMBER_OP_NOTICE: Member change: vc add of member 1"
}
        '''
        tmp = self.event_type.split("_")
        action = tmp[len(tmp)-1]
        self.text = f"MEMBER #{action} to the Virtual Chassis \"{self.device_name}\" (MAC: {self.device_mac})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""

    def _sw_master_rec(self):
        '''
{
    "timestamp": 1599046353,
    "org_id": "b4e16c72-d50e-4c03-a952-a3217e231e2c",
    "site_id": "2102aa05-b1ae-4d2d-88dc-c1bf9d834b9e",
    "type": "SW_MASTER_ON_RECOVERY",
    "model": "EX2300-C-12P",
    "device_type": "switch",
    "text": "Device is running on recovery partition",
    "version": "20.2R3.9",
    "mac": "f4cc552aba80"
}
        '''
        self.text = f"The MASTER of the Virtual Chassis \"{self.device_name}\" (MAC: {self.device_mac})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""
        self.text += " IS ON RECOVERY PARTITION"

    def _sw_member_rec(self):
        '''
{
    "type": "SW_VC_MEMBER_ADDED",
    "site_id": "f688779c-e335-4f88-8d7c-9c5e9964528b",
    "org_id": "b4e16c72-d50e-4c03-a952-a3217e231e2c",
    "mac": "1c9c8cba2e7f",
    "version": "18.2R3.4",
    "text": "CHASSISD_VCHASSIS_MEMBER_OP_NOTICE: Member change: vc add of member 1"
}
        '''
        self.text = f"MEMBER of the Virtual Chassis \"{self.device_name}\" (MAC: {self.device_mac})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""
        self.text += " IS ON RECOVERY PARTITION"

    def _sw_snapshot(self):
        '''
{
    "timestamp": 1599046353,
    "org_id": "b4e16c72-d50e-4c03-a952-a3217e231e2c",
    "site_id": "2102aa05-b1ae-4d2d-88dc-c1bf9d834b9e",
    "type": "SW_RECOVERY_SNAPSHOT_REQUESTED",
    "model": "EX2300-C-12P",
    "device_type": "switch",
    "version": "20.2R3.9",
    "mac": "f4cc552aba80"
}
        '''
        tmp = self.event_type.split("_")
        action = tmp[len(tmp)-1]
        self.text = f"RECOVERY SNAPSHOT {action} for the Switch \"{self.device_name}\" (MAC: {self.device_mac})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""

    def _sw_snapshot_notneeded(self):
        '''
{
    "timestamp": 1599046353,
    "org_id": "b4e16c72-d50e-4c03-a952-a3217e231e2c",
    "site_id": "2102aa05-b1ae-4d2d-88dc-c1bf9d834b9e",
    "type": "SW_RECOVERY_SNAPSHOT_REQUESTED",
    "model": "EX2300-C-12P",
    "device_type": "switch",
    "version": "20.2R3.9",
    "mac": "f4cc552aba80"
}
        '''
        self.text = f"RECOVERY SNAPSHOT NOT NEEDED for the Switch \"{self.device_name}\" (MAC: {self.device_mac})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""

    def _sw_snapshot_unsported(self):
        '''
{
    "timestamp": 1599046353,
    "org_id": "b4e16c72-d50e-4c03-a952-a3217e231e2c",
    "site_id": "2102aa05-b1ae-4d2d-88dc-c1bf9d834b9e",
    "type": "SW_RECOVERY_SNAPSHOT_REQUESTED",
    "model": "EX2300-C-12P",
    "device_type": "switch",
    "version": "20.2R3.9",
    "mac": "f4cc552aba80"
}
        '''
        self.text = f"RECOVERY SNAPSHOT UNSUPPORTED by the Switch \"{self.device_name}\" (MAC: {self.device_mac})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""

    def _sw_dot1x_user(self):
        '''
{
    "device_name": "sw-jn-02.lab",
    "device_type": "switch",
    "mac": "2c21311c37b0",
    "org_id": "203d3d02-dbc0-4c1b-9f41-76896a3330f4",
    "site_id": "f5fcbee5-fbca-45b3-8bf1-1619ede87879",
    "site_name": "BR-Spoke-01",
    "text": "DOT1XD_USR_AUTHENTICATED: Custom_log MAC-RADIUS User b827eb93afac logged in MacAddress b8:27:eb:93:af:ac interface ge-0/0/7.0 vlan srv",
    "timestamp": 1652773155,
    "type": "SW_DOT1XD_USR_AUTHENTICATED"
}
'''
        self.text = f"NEW DOT1X AUTHENTICATION on the Switch \"{self.device_name}\" (MAC: {self.device_mac})"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""

    def _sw_radius_unreachable(self):
        '''
{
    "device_name": "sw-jn-02.lab",
    "device_type": "switch",
    "mac": "2c21311c37b0",
    "org_id": "203d3d02-dbc0-4c1b-9f41-76896a3330f4",
    "site_id": "f5fcbee5-fbca-45b3-8bf1-1619ede87879",
    "site_name": "BR-Spoke-01",
    "text": "AUTHD_RADIUS_SERVER_STATUS_CHANGE: Status of radius server 10.3.20.2 set to UNREACHABLE (profile dot1x)",
    "timestamp": 1653305242,
    "type": "SW_RADIUS_SERVER_UNREACHABLE"
}        
        '''
        self.text = f"Switch \"{self.device_name}\" (MAC: {self.device_mac}) in unable to reach the RADIUS server"
        if self.site_name:
            self.text += f" on site \"{self.site_name}\""