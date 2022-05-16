from .alarm_common import CommonAlarm


class SecurityAlarm(CommonAlarm):

    def __init__(self, mist_host, alarm_channels, event):
        self.wlan_ids = event.get("wlan_ids", [])
        self.bssids = event.get("bssids", [])
        self.ssids = event.get("ssids", [])
        self.client_macs = event.get("client_macs", [])
        CommonAlarm.__init__(self, mist_host, alarm_channels, event)

    def _process(self):
        if self.alarm_type == "secpolicy_violation":
            self._secpolicy_violation()
        elif self.alarm_type in "bssid_spoofing":
            self._security_ssid()
        elif self.alarm_type == "honeypot_ssid":
            self._security_ssid()
        elif self.alarm_type == "adhoc_network":
            self._security_ssid()
        elif self.alarm_type == "rogue_ap":
            self._security_ssid()
        elif self.alarm_type == "rogue_client":
            self._security_ssid()
        elif self.alarm_type == "watched_station":
            self._security_ssid()
        elif self.alarm_type == "eap_handshake_flood":
            self._security_ssid()
        elif self.alarm_type == "air_magnet_scan":
            self._security_ssid()
        elif self.alarm_type == "excessive_eapol_start":
            self._security_ssid()
        elif self.alarm_type == "eapol_logoff_attack":
            self._security_ssid()
        elif self.alarm_type == "eap_dictionary_attack":
            self._security_ssid()
        elif self.alarm_type == "disassociation_flood":
            self._security_ssid()
        elif self.alarm_type == "beacon_flood":
            self._security_ssid()
        elif self.alarm_type == "essid_jack":
            self._security_ssid()
        elif self.alarm_type == "krack_attack":
            self._security_ssid()
        elif self.alarm_type == "vendor_ie_missing":
            self._security_ssid()
        elif self.alarm_type == "tkip_icv_attack":
            self._security_ssid()
        elif self.alarm_type == "repeated_auth_failures":
            self._security_ssid()
        elif self.alarm_type == "eap_failure_injection":
            self._security_ssid()
        elif self.alarm_type == "eap_spoofed_success":
            self._security_ssid()
        elif self.alarm_type == "out_of_sequence":
            self._security_ssid()
        elif self.alarm_type == "zero_ssid_association":
            self._security_ssid()
        elif self.alarm_type == "monkey_jack":
            self._security_ssid()
        elif self.alarm_type == "excessive_client":
            self._security_ssid()
        elif self.alarm_type == "ssid_injection":
            self._security_ssid()
        else:
            self._common()

    def _secpolicy_violation(self):
        '''
        {
            "id": "8d2ae972-4339-4db4-bad7-a9440c72dd90",
            "org_id": "688605f-916a-47a1-8c68-f19618300a08",
            "site_id": "ec3b5624-73f1-4ed3-b3fd-5ba3ee40368a",
            "type": "secpolicy_violation",
            "group": "security",
            "severity": "warn",
            "timestamp": 1633084683,
            "last_seen": 1633084683,
            "secpolicy_violated": true,
            "aps": [
                "5c5b350f3208"
            ],
            "wlan_ids": [
                "1bf047be-9819-445c-a531-d6637a3736b3"
            ],
            "count": 1
        }
        '''

        self.text = f"SECURITY - SECPOLICY VIOLATED on site {self.site_name}"
        if self.count == 1:
            self.text += " 1 time"
        elif self.count:
            self.text += f" {self.count} times"
        if len(self.aps) == 1:
            self.text += " by 1 AP"
        elif len(self.aps) > 1:
            self.text += f" by {len(self.aps)} APs"
        if len(self.wlan_ids) == 1:
            self.text += " on 1 WLAN"
        elif len(self.wlan_ids) > 1:
            self.text += f" on {len(self.wlan_ids)} WLANs"
        self.info.append(f"*APs*: {', '.join(self.aps)}")
        self.info.append(f"*WLANs*: {', '.join(self.wlan_ids)}")

    def _security_ssid(self):
        '''
        '''
        self.text = f"SECURITY - {self.alarm_type.replace('_', ' ').upper()} detected on site {self.site_name}"
        if self.aps:
            self.info.append(f"*APs*: {', '.join(self.aps)}")
        if self.bssids:
            self.info.append(
                f"*BSSIDS*: {', '.join(self.bssids)}")
        if self.ssids:
            self.info.append(
                f"*SSIDS*: {', '.join(self.ssids)}")
        if self.hostnames:
            self.info.append(
                f"*HOSTNAMES*: {', '.join(self.hostnames)}")
        if self.client_macs:
            self.info.append(
                f"*CLIENT MACS*: {', '.join(self.client_macs)}")
