from datetime import datetime
from .alarm_common import CommonAlarm


class MarvisAlarm(CommonAlarm):

    def __init__(self, mist_host, alarm_channels, event):
        self.email = None
        self.category = None
        self.status = "UNKNOWN"
        self.action = None
        self.symptom = None

        if "email_content" in event:
            self.email = event["email_content"]
            self.category = event["email_content"].get("category", None)
        if "details" in event:
            self.status = event["details"].get("status", None)
            self.action = event["details"].get("action", None)
            self.symptom = event["details"].get("symptom", None)
        CommonAlarm.__init__(self, mist_host, alarm_channels, event)

    def _process(self):
        if self.alarm_type in [
            "missing_vlan",
            "bad_cable", "gw_bad_cable", "ap_bad_cable",
            "authentication_failure", "dhcp_failure", "arp_failure", "dns_failure",
            "port_flap",
            "negotiation_mismatch", "gw_negotiation_mismatch",
            "ap_offline",
            "non_compliant",
            "health_check_failed"
        ]:
            self._marvis()
        else:
            self._common()

    def _marvis(self):
        """
        """
        self.text = f"MARVIS {self.alarm_type.replace('_', ' ').upper()} issue on site {self.site_name}"
        done = []
        if self.category:
            self.info.append(f"*CATEGORY*: {self.category}")
            done.append("category")
        if self.status:
            self.info.append(f"*STATUS*: {self.status}")
            done.append("status")
        if self.action:
            self.info.append(f"*ACTION*: {self.action}")
            done.append("action")
        if self.symptom:
            self.info.append(f"*SYMPTOM*: {self.symptom}")
            done.append("symptom")
        if self.email:
            for entry in self.email:
                if not entry in done:
                    if isinstance(self.email[entry], list):
                        self.info.append(
                            f"*{entry.replace('_', ' ').upper()}*: {', '.join(self.email[entry])}")
                    else:
                        self.info.append(
                            f"*{entry.replace('_', ' ').upper()}*: {self.email[entry]}")
