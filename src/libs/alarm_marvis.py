from datetime import datetime
from .alarm_common import CommonAlarm


class MarvisAlarm(CommonAlarm):

    def __init__(self, mist_host, alarm_channels, event):
        CommonAlarm.__init__(self, mist_host, alarm_channels, event)
        self.display =  {
            "missing_vlan": "Missing VLAN",
            "bad_cable": "Bad cable",
            "port_flap": "Port flap",
            "gw_bad_cable": "Bad cable",
            "authentication_failure": "Authentication failure",
            "dhcp_failure": "DHCP failure",
            "arp_failure": "ARP failure",
            "dns_failure": "DNS failure",
            "negotiation_mismatch": "Negotiation mismatch",
            "gw_negotiation_mismatch": "Negotiation mismatch",
            "ap_offline": "Offline",
            "non_compliant": "Non-compliant",
            "ap_bad_cable": "Bad cable",
            "health_check_failed": "AP health check failed"
        }

    def _process(self):
            self._marvis()


    def _marvis(self):
        """
        {
            "severity": "critical",
            "timestamp": 1631854164,
            "last_seen": 1631854164,
            "org_id": "1688605f-916a-47a1-8c68-f19618300a08",
            "site_id": "ec3b5624-73f1-4ed3-b3fd-5ba3ee40368a",
            "count": 1,
            "id": "bb1aa333-b2c8-4afa-8a43-103f94919be6",
            "type": "authentication_failure",
            "group": "marvis"
        }
        """
        display = self.display[self.event["type"]]
        text_string = "Marvis has reported "
        if (self.event["count"] > 1):
            text_string += self.event["count"] + " new " + display + " issues"
        else:
            text_string += self.event["count"] + " new " + display + " issue"
        if "timestamp" in self.event:
            text_string += " at {0}".format(
                datetime.fromtimestamp(self.event["timestamp"]))
        self.text.append(text_string)

 