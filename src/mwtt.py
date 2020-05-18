
### WEB SERVER IMPORTS ###
from flask import Flask
from flask import json
from flask import request
### OTHER IMPORTS ###
import json
from libs import req
import os
import time

###########################
### LOADING SETTINGS
from config import mist_conf
from config import slack_conf
from config import msteams_conf
from config import color_config
from config import message_levels

apitoken = mist_conf["apitoken"]
mist_cloud = mist_conf["mist_cloud"]
server_uri = mist_conf["server_uri"]
site_id_ignored = mist_conf["site_id_ignored"]

from libs.slack import Slack
slack = Slack(slack_conf, message_levels)
from libs.msteams import Teams
teams = Teams(msteams_conf)
###########################
### LOGGING SETTINGS
try:
    from config import log_level
except:
    log_level = 6
finally:
    from libs.debug import Console
    console = Console(log_level)


###########################
### VARS
try:
    from config import port as server_port
except:
    server_port = 51361

###########################
### FUNCTIONS
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
        
def new_event(topic, event):
    console.info("%s" %topic)
    message = []
    for key in event:
        console.info("%s: %s\r" %(key, event[key]))
        message.append("%s: %s" %(key, event[key]))
        if topic in color_config:
            color = color_config[topic]
        else:
            color = None
        if key == "type":
            topic2 += " - %s" %(event[key])
        else:
            topic2 = topic
    if slack_conf["enabled"]: slack.send_manual_message(topic, message, event, color)
    if msteams_conf["enabled"]: teams.send_manual_message(topic2, message, color)
###########################
### ENTRY POINT
app = Flask(__name__)
@app.route(server_uri, methods=["POST"])
def postJsonHandler():
    content = request.get_json()
    topic = content["topic"]
    events = content["events"]
    for event in events:   
        new_event(topic, event)
    return '', 200


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=server_port)


