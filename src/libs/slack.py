from libs import req
import requests
import json
import time
from datetime import datetime, timedelta


class Slack:

    def __init__(self, config, message_levels):
        if config:
            self.enabled = config["enabled"]
            self.url_debug = config["url_debug"]
            self.url_info = config["url_info"]
            self.url_warning = config["url_warning"]
            self.url_unknown = config["url_unknown"]
            self.allowed_admins = config["allowed_admins"]
            self.message_levels = message_levels
        self.severity = 7
        self.color = {
            "green": "#36a64f",
            "blue": "#2196f3",
            "orange": "warning",
            "red": "danger"

        }

    def _get_color(self):
        if self.severity >= 6:
            return self.color["green"]
        elif self.severity >= 5:
            return self.color["blue"]
        elif self.severity >= 4:
            return self.color["orange"]
        else:
            return self.color["red"]

    def _generate_button(self, tag, text, url):
        return {
                    "name": tag,
					"type": "button",
					"text": {
						"text": text
					},
					"style": "primary",
					"url": url
				}

    def _audit(self, event, color):
        org_id = None
        site_id = None
        url = None
        actions = []
        message = None

        if "admin_name" in event:
            admin = event["admin_name"]
        if "src_ip" in event:
            src_ip = event["src_ip"]
        if "message" in event:
            message = event["message"]
        if "org_id" in event:
            org_id = event["org_id"]
        if "site_id" in event:
            site_id = event["site_id"]
        # if "wxtunnel_id" in event:
        # if "wxrules_id" in event:
        if "wxtag_id" in event:
            if site_id:
                url = "https://manage.mist.com/admin/?org_id=%s#!tags/detail/%s/%s" % (
                    org_id, event["wlan_id"], site_id)
                actions.append(self._generate_button("wxtag", "See Tag", url))
            else:
                url = "https://manage.mist.com/admin/?org_id=%s#!orgTags/detail/%s/%s" % (
                    org_id, event["wlan_id"], org_id)
                actions.append(self._generate_button("wxtag", "See Tag", url))
        if "wlan_id" in event:
            if site_id:
                url = "https://manage.mist.com/admin/?org_id=%s#!wlan/detail/%s/%s" % (org_id, event["wlan_id"], site_id)
                actions.append(self._generate_button("wlan", "See WLAN", url))
        if "ticket_id" in event:
            url = "https://manage.mist.com/admin/?org_id=%s#!tickets/ticket/%s/%s" % (org_id, event["ticket_id"], org_id)
            actions.append(self._generate_button("ticket", "See Ticket", url))
        if "template_id" in event:
            url = "https://manage.mist.com/admin/?org_id=%s#!templates/template/%s" % (org_id, event["template_id"])
            actions.append(self._generate_button("template", "See Template", url))
        # if "sitegroup_id" in event:
        # if "secpolicy_id" in event:
        if "rftemplate_id" in event:
            url = "https://manage.mist.com/admin/?org_id=%s#!rftemplates/rftemplate/%s" % (org_id, event["rftemplate_id"])
            actions.append(self._generate_button("rftemplate", "See RF Template", url))
        # if "psk_id" in event:
        # if "networktemplate_id" in event:
        if "mxtunnel_id" in event:
            url = "https://manage.mist.com/admin/?org_id=%s#!mistTunnels/detail/%s" % (org_id, event["mxtunnel_id"])
            actions.append(self._generate_button("mxtunnel", "See Mist Tunnel", url))
        if "mxcluster_id" in event:
            url = "https://manage.mist.com/admin/?org_id=%s#!edge/clusterdetail/%s" % (org_id, event["mxcluster_id"])
            actions.append(self._generate_button("mxcluster", "See Cluster", url))
        if "mxedge_id" in event:
            url = "https://manage.mist.com/admin/?org_id=%s#!edge/edgedetail/%s" % (org_id, event["mxedge_id"])
            actions.append(self._generate_button("mxedge", "See mxEdge", url))
        # if "assetfilter_id" in event:
        if "deviceprofile_id" in event:
            url = "https://manage.mist.com/admin/?org_id=%s#!deviceProfiles/detail/%s" % (org_id, event["deviceprofile_id"])
            actions.append(self._generate_button("deviceprofile", "See Device Profile", url))
        if "device_id" in event:
            if site_id:
                url = "https://manage.mist.com/admin/?org_id=%s#!ap/detail/%s/%s" % (org_id, event["device_id"], site_id)
                actions.append(self._generate_button("device", "See Device", url))
            else:
                url = "https://manage.mist.com/admin/?org_id=%s#!apInventory" % (org_id)
                actions.append(self._generate_button("inventory", "See Inventory", url))

        if "Reboot Device" in message or "ssign Device" in message:
            if site_id:
                url = "https://manage.mist.com/admin/?org_id=%s#!ap/%s" %(org_id, site_id)
                actions.append(self._generate_button("device", "See Devices", url))
            else:
                url = "https://manage.mist.com/admin/?org_id=%s#!apInventory" % (org_id)
                actions.append(self._generate_button("inventory", "See Inventory", url))


        if admin.split(" ")[-1:][0] in self.allowed_admins:
            slack_url = self.url_info
            # if event["type"] in self.message_levels["device-events"]["warning"]:
            #     slack_url = self.url_warning
            # elif event["type"] in self.message_levels["device-events"]["info"]:
            #     slack_url = self.url_info
            # elif event["type"] in self.message_levels["device-events"]["debug"]:
            #     slack_url = self.url_debug
            # else:
            #     slack_url = self.url_unknown
        else:
            slack_url = self.url_warning


        attachments = [{
                    "fallback": "New MWTT event",
                    "color": color,
                    "text": "Admin: %s (IP: %s)\rAction: %s" % (admin, src_ip, message),
                    "attachment_type": "default",
                    "actions": actions
                }]

        return [slack_url, attachments]

    def _device_event(self, topic, event, color):
        org_id = None
        site_id = None
        ap = None
        text = ""
        actions = []
        d_stop = datetime.now()
        d_start = d_stop - timedelta(days=1)
        t_stop= int(datetime.timestamp(d_stop))
        t_start= int(datetime.timestamp(d_start))

        if "org_id" in event:
            org_id = event["org_id"]
        if "site_id" in event:
            site_id = event["site_id"]
        if "ap" in event:
            ap = event["ap"]
            ap_id= "00000000-0000-0000-1000-%s" % (ap)
        if "ap_name" in event:
            text = "AP Name: %s\r" %(event["ap_name"])
        text += "AP MAC: %s\r" %(event["ap"])
        if "site_name" in event:
            text += "Site: %s\r" %(event["site_name"])
        text += "Event: %s\r" %(event["type"])
        if "reason" in event:
            text += "Reason: %s\r" %(event["reason"])


        if "audit_id" in event:
            url_audit= "https://manage.mist.com/admin/?org_id=%s#!auditLogs" % (org_id)
            actions.append(self._generate_button("audit", "Audit Logs", url_audit))
        if not event["type"] == "AP_UNASSIGNED":
            url_insights= "https://integration.mist.com/admin/?org_id=%s#!dashboard/insights/device/%s/today/%s/%s/%s" % (org_id, ap_id, t_start, t_stop, site_id)
            actions.append(self._generate_button("insights", "AP Insights", url_insights))
            url_conf = "https://manage.mist.com/admin/?org_id=%s#!ap/detail/%s/%s" %(org_id, ap_id, site_id)
            actions.append(self._generate_button("insights", "AP Configuration", url_conf))

        if event["type"] in self.message_levels["device-events"]["warning"]:
            slack_url = self.url_warning
        elif event["type"] in self.message_levels["device-events"]["info"]:
            slack_url = self.url_info
        elif event["type"] in self.message_levels["device-events"]["debug"]:
            slack_url = self.url_debug
        else:
            slack_url = self.url_unknown

        attachments= [{
                    "fallback": "New MWTT event",
                    "color": color,
                    "text": text,
                    "attachment_type": "default",
                    "actions": actions
                }]

        return [slack_url, attachments]

    def send_manual_message(self, topic, message, event, color="#000000"):

        now = datetime.now()
        now.strftime("%d/%m/%Y %H:%M:%S")
        title = "%s - %s" % (now, topic)

        if topic == "audits":
            slack_url, attachments = self._audit(event, color)
        elif topic == "device-events":
            slack_url, attachments = self._device_event(topic, event, color)
        else:
            message_string = ""
            for mpart in message:
                message_string += "%s\r" % (mpart)
            slack_url = self.url_unknown
            attachments = [
                    {
                        "fallback": "New MWTT event",
                        "color": color,
                        "text": message_string,
                "attachment_type": "default"  
                    }
                ]              


        body = {
            "text": title,
            "attachments": attachments
        }

        print(event)
        print(topic)
        print(message)
        print("------")
        
        data = json.dumps(body)
        data = data.encode("ascii")
        requests.post(slack_url, headers={
                      "Content-type": "application/json"}, data=data)
