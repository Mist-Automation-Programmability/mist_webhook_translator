

def audit(mist_host, approved_admins, audit_channels, event):
    mist_dashboard = mist_host.replace("api", "manage")
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

    actions.append({"tag": "logs", "text": "See Audit Logs", "url": f"https://manage.mist.com/admin/?org_id={org_id}#!auditLogs"})
    # if "wxtunnel_id" in event:
    # if "wxrules_id" in event:
    if "wxtag_id" in event:
        if site_id:
            url = f"fhttps://{mist_dashboard}/admin/?org_id={org_id}#!tags/detail/{event['wlan_id']}/{site_id}"
            actions.append({"tag": "wxtag", "text":  "See Tag", "url": url})
        else:
            url = f"https://{mist_dashboard}/admin/?org_id={org_id}#!orgTags/detail/{event['wlan_id']}/{org_id}"
            actions.append({"tag": "wxtag", "text":  "See Tag", "url": url})
    if "wlan_id" in event:
        if site_id:
            url = f"https://{mist_dashboard}/admin/?org_id={org_id}#!wlan/detail/{event['wlan_id']}/{org_id}"
            actions.append({"tag": "wlan", "text":  "See WLAN", "url": url})
    if "ticket_id" in event:
        url = f"https://{mist_dashboard}/admin/?org_id={org_id}#!tickets/ticket/{event['ticket_id']}/{org_id}"
        actions.append({"tag": "ticket", "text":  "See Ticket", "url": url})

    if "gatewaytemplate_id" in event:
        url = f"https://{mist_dashboard}/admin/?org_id={org_id}#!gatewayTemplates/detail/{event['gatewaytemplate_id']}"
        actions.append(
            {"tag": "gatewaytemplate", "text":  "See Gateway Template", "url": url})
    elif "template_id" in event:
        url = f"https://{mist_dashboard}/admin/?org_id={org_id}#!templates/template/{event['template_id']}"
        actions.append({"tag": "networktemplate", "text":  "See Template", "url": url})
    elif "rftemplate_id" in event:
        url = f"https://{mist_dashboard}/admin/?org_id={org_id}#!rftemplates/rftemplate/{event['rftemplate_id']}"
        actions.append(
            {"tag": "rftemplate", "text":  "See RF Template", "url": url})
    elif "networktemplate_id" in event:
        url = f"https://{mist_dashboard}/admin/?org_id={org_id}#!switchTemplate/detail/{event['networktemplate_id']}"
        actions.append(
            {"tag": "networktemplate", "text":  "See Switch Template", "url": url})

    # if "sitegroup_id" in event:
    # if "secpolicy_id" in event:
    # if "psk_id" in event:
    if "mxtunnel_id" in event:
        url = f"https://{mist_dashboard}/admin/?org_id={org_id}#!mistTunnels/detail/{event['mxtunnel_id']}"
        actions.append(
            {"tag": "mxtunnel", "text":  "See Mist Tunnel", "url": url})
    if "mxcluster_id" in event:
        url = f"https://{mist_dashboard}/admin/?org_id={org_id}#!edge/clusterdetail/{event['mxcluster_id']}"
        actions.append({"tag": "mxcluster", "text":  "See Cluster", "url": url})
    if "mxedge_id" in event:
        url = f"https://{mist_dashboard}/admin/?org_id={org_id}#!edge/edgedetail/{event['mxedge_id']}"
        actions.append({"tag": "mxedge", "text":  "See mxEdge", "url": url})
    # if "assetfilter_id" in event:
    if "deviceprofile_id" in event:
        url = f"https://{mist_dashboard}/admin/?org_id={org_id}#!deviceProfiles/detail/{event['deviceprofile_id']}"
        actions.append(
            {"tag": "deviceprofile", "text":  "See Device Profile", "url": url})
    if "device_id" in event:
        if site_id:
            url = f"https://{mist_dashboard}/admin/?org_id={org_id}#!ap/detail/{event['device_id']}/{site_id}"
            actions.append({"tag": "device", "text":  "See Device", "url": url})
        else:
            url = f"https://{mist_dashboard}/admin/?org_id={org_id}#!apInventory"
            actions.append(
                {"tag": "device", "text":  "See Inventory", "url": url})

    if "Reboot Device" in message or "ssign Device" in message:
        if site_id:
            url = f"https://{mist_dashboard}/admin/?org_id={org_id}#!ap/{site_id}"
            actions.append(
                {"tag": "action", "text":  "See Devices", "url": url})
        else:
            url = f"https://{mist_dashboard}/admin/?org_id={org_id}#!apInventory"
            actions.append(
                {"tag": "action", "text":  "See Inventory", "url": url})

    if admin.split(" ")[-1:][0] in approved_admins:
        channel = audit_channels["approved_admins"]
    else:
        channel = audit_channels["other_admins"]

    text = message
    info = [
        f"*Admin*: {admin}",
        f"*IP*: {src_ip}"
    ]
    #text = [f"Admin: {admin} (IP: {src_ip})", f"Action: {message}"]
    print({
        "channel": channel,
        "title": "AUDIT LOGS",
        "text": text,
        "info": info,
        "actions": actions
    })
    return {
        "channel": channel,
        "title": "AUDIT LOGS",
        "text": text,
        "info": info,
        "actions": actions
    }
