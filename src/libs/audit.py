
def get_device_type(self, mist_host, side_id, device_id):
    api_host = mist_host.replace("manage", "api")
def audit(self, mist_host, approved_admins, event):
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


    if admin.split(" ")[-1:][0] in approved_admins:
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