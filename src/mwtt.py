
### WEB SERVER IMPORTS ###
from flask import Flask
from flask import json
from flask import request
### OTHER IMPORTS ###
import json
from libs import req
import os
import time
from datetime import datetime, timedelta
###########################
### LOADING SETTINGS
from config import mist_conf
from config import slack_conf
from config import msteams_conf
from config import color_config
from config import message_levels

apitoken = mist_conf["apitoken"]
mist_host = mist_conf["mist_host"]
server_uri = mist_conf["server_uri"]
site_id_ignored = mist_conf["site_id_ignored"]

from libs.slack import Slack
slack = Slack(slack_conf)
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
def _audit(self, event):
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
            url = "https://%s/admin/?org_id=%s#!tags/detail/%s/%s" % (mist_host,
                org_id, event["wlan_id"], site_id)
            actions.append({"tag": "wxtag", "text":  "See Tag", "url": url})
        else:
            url = "https://%s/admin/?org_id=%s#!orgTags/detail/%s/%s" % (mist_host,
                org_id, event["wlan_id"], org_id)
            actions.append({"tag": "wxtag", "text":  "See Tag", "url": url})
    if "wlan_id" in event:
        if site_id:
            url = "https://%s/admin/?org_id=%s#!wlan/detail/%s/%s" % (mist_host,org_id, event["wlan_id"], site_id)
            actions.append({"tag": "wxtag", "text":  "See WLAN", "url": url})
    if "ticket_id" in event:
        url = "https://%s/admin/?org_id=%s#!tickets/ticket/%s/%s" % (mist_host,org_id, event["ticket_id"], org_id)
        actions.append({"tag": "wxtag", "text":  "See Ticket", "url": url})
    if "template_id" in event:
        url = "https://%s/admin/?org_id=%s#!templates/template/%s" % (mist_host,org_id, event["template_id"])
        actions.append({"tag": "wxtag", "text":  "See Template", "url": url})
    # if "sitegroup_id" in event:
    # if "secpolicy_id" in event:
    if "rftemplate_id" in event:
        url = "https://%s/admin/?org_id=%s#!rftemplates/rftemplate/%s" % (mist_host,org_id, event["rftemplate_id"])
        actions.append({"tag": "wxtag", "text":  "See RF Template", "url": url})
    # if "psk_id" in event:
    # if "networktemplate_id" in event:
    if "mxtunnel_id" in event:
        url = "https://%s/admin/?org_id=%s#!mistTunnels/detail/%s" % (mist_host,org_id, event["mxtunnel_id"])
        actions.append({"tag": "wxtag", "text":  "See Mist Tunnel", "url": url})
    if "mxcluster_id" in event:
        url = "https://%s/admin/?org_id=%s#!edge/clusterdetail/%s" % (mist_host,org_id, event["mxcluster_id"])
        actions.append({"tag": "wxtag", "text":  "See Cluster", "url": url})
    if "mxedge_id" in event:
        url = "https://%s/admin/?org_id=%s#!edge/edgedetail/%s" % (mist_host,org_id, event["mxedge_id"])
        actions.append({"tag": "wxtag", "text":  "See mxEdge", "url": url})
    # if "assetfilter_id" in event:
    if "deviceprofile_id" in event:
        url = "https://%s/admin/?org_id=%s#!deviceProfiles/detail/%s" % (mist_host,org_id, event["deviceprofile_id"])
        actions.append({"tag": "wxtag", "text":  "See Device Profile", "url": url})
    if "device_id" in event:
        if site_id:
            url = "https://%s/admin/?org_id=%s#!ap/detail/%s/%s" % (mist_host,org_id, event["device_id"], site_id)
            actions.append({"tag": "wxtag", "text":  "See Device", "url": url})
        else:
            url = "https://%s/admin/?org_id=%s#!apInventory" % (mist_host,org_id)        
            actions.append({"tag": "wxtag", "text":  "See Inventory", "url": url})

    if "Reboot Device" in message or "ssign Device" in message:
        if site_id:
            url = "https://%s/admin/?org_id=%s#!ap/%s" %(mist_host,org_id, site_id)
            actions.append({"tag": "wxtag", "text":  "See Devices", "url": url})
        else:
            url = "https://%s/admin/?org_id=%s#!apInventory" % (mist_host,org_id)
            actions.append({"tag": "wxtag", "text":  "See Inventory", "url": url})


    if admin.split(" ")[-1:][0] in mist_conf["approved_admins"]:
        level = "info"
        # if event["type"] in self.message_levels["device-events"]["warning"]:
        #     slack_url = self.url_warning
        # elif event["type"] in self.message_levels["device-events"]["info"]:
        #     slack_url = self.url_info
        # elif event["type"] in self.message_levels["device-events"]["debug"]:
        #     slack_url = self.url_debug
        # else:
        #     slack_url = self.url_unknown
    else:
        level = "warning"

    text = ["Admin: %s (IP: %s)" %(admin, src_ip), "Action: %s" %(message)]

    return [level, text, actions]

def _device_event(topic, event):
    org_id = None
    site_id = None
    ap = None
    text = []
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
        text.append("AP Name: %s" %(event["ap_name"]))
    text.append("AP MAC: %s" %(event["ap"]))
    if "site_name" in event:
        text.append("Site: %s" %(event["site_name"]))
    text.append("Event: %s" %(event["type"]))
    if "reason" in event:
        text.append("Reason: %s" %(event["reason"]))


    if "audit_id" in event:
        url_audit= "https://%s/admin/?org_id=%s#!auditLogs" % (mist_host,org_id)
        actions.append({"tag": "audit", "text": "Audit Logs", "url": url_audit})
    if not event["type"] == "AP_UNASSIGNED":
        url_insights= "https://%s/admin/?org_id=%s#!dashboard/insights/device/%s/24h/%s/%s/%s" % (mist_host,org_id, ap_id, t_start, t_stop, site_id)
        actions.append({"tag": "insights", "text": "AP Insights", "url": url_insights})
        url_conf = "https://%s/admin/?org_id=%s#!ap/detail/%s/%s" %(mist_host,org_id, ap_id, site_id)
        actions.append({"tag": "insights", "text": "AP Configuration", "url": url_conf})

    if event["type"] in message_levels["device-events"]["warning"]:
        level = "warning"
    elif event["type"] in message_levels["device-events"]["info"]:
        level = "info"
    elif event["type"] in message_levels["device-events"]["debug"]:
        level = "debug"
    else:
        level = "unknown"


    return [level, text, actions]

def _title(topic):
    now = datetime.now()
    now.strftime("%d/%m/%Y %H:%M:%S")
    return "%s - %s" % (now, topic)

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

    if topic == "audits":
        level, text, actions = _audit(topic, event)
    elif topic == "device-events":
        level, text, actions = _device_event(topic, event)
    else:
        text = ""
        level = "unknown"
        actions = []
        for mpart in message:
            text += "%s\r" % (mpart)        


    if slack_conf["enabled"]: slack.send_manual_message(_title(topic), text, level, color, actions)
    if msteams_conf["enabled"]: teams.send_manual_message(topic, str(datetime.now()), text, level, color, actions)
    print(event)
    print(topic)
    print(message)
    print("------")




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


