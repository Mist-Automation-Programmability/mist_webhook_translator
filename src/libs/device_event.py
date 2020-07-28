from datetime import datetime, timedelta

def device_event(topic, mist_host, message_levels, event):
    org_id = None
    site_id = None
    ap = None
    text = []
    actions = []
    d_stop = datetime.now()
    d_start = d_stop - timedelta(days=1)
    t_stop= int(datetime.timestamp(d_stop))
    t_start= int(datetime.timestamp(d_start))

    org_id, site_id, site_name, ap_mac, ap_id, ap_name, event_type, reason, audit_id = _extract_fields(event)

    if event_type == "AP_CONFIG_CHANGED_BY_RRM":
        text = _ap_config_changed_by_rrm(ap_mac, ap_name, site_name)
    elif event_type == "AP_CONFIG_CHANGED_BY_USER":
        text = _ap_config_changed_by_rrm(ap_mac, ap_name, site_name)
    elif event_type == "1026":
        text = _1026(ap_mac, ap_name, site_name, reason)
    elif event_type == "AP_CONFIGURED":
        text = _ap_common(ap_mac, ap_name, site_name, event_type)
    elif event_type == "AP_RECONFIGURED":
        text = _ap_common(ap_mac, ap_name, site_name, event_type)
    elif event_type == "AP_RESTARTED":
        text = _ap_common(ap_mac, ap_name, site_name, event_type)
    elif event_type == "AP_RESTART_BY_USER":
        text = _ap_common(ap_mac, ap_name, site_name, event_type)
    elif event_type == "AP_CONNECTED":
        text = _ap_common(ap_mac, ap_name, site_name, event_type)
    elif event_type == "AP_DISCONNECTED":
        text = _ap_common(ap_mac, ap_name, site_name, event_type)
    elif event_type == "AP_ASSIGNED":
        text = _ap_assigned(ap_mac, ap_name, site_name)
    elif event_type == "AP_UNASSIGNED":
        text = _ap_unassigned(ap_mac, ap_name, site_name)
    else:
        text.append("AP Name: %s" %(ap_name))
        text.append("AP MAC: %s" %(ap))
        text.append("Site: %s" %(site_name))
        text.append("Event: %s" %(event_type))
        text.append("Reason: %s" %(reason))

    if audit_id:
        text.append("Check the audit logs for more details.")

    if "audit_id" in event:
        url_audit= "https://%s/admin/?org_id=%s#!auditLogs" % (mist_host,org_id)
        actions.append({"tag": "audit", "text": "Audit Logs", "url": url_audit})
    if not event["type"] == "AP_UNASSIGNED":
        url_insights= "https://%s/admin/?org_id=%s#!dashboard/insights/device/%s/24h/%s/%s/%s" % (mist_host,org_id, ap_id, t_start, t_stop, site_id)
        actions.append({"tag": "insights", "text": "AP Insights", "url": url_insights})
        url_conf = "https://%s/admin/?org_id=%s#!ap/detail/%s/%s" %(mist_host,org_id, ap_id, site_id)
        actions.append({"tag": "insights", "text": "AP Configuration", "url": url_conf})

    if event["type"] in message_levels["warning"]:
        level = "warning"
    elif event["type"] in message_levels["info"]:
        level = "info"
    elif event["type"] in message_levels["debug"]:
        level = "debug"
    else:
        level = "unknown"


    return [level, text, actions]

def _extract_fields(event):
    org_id = None
    site_id = None
    ap_mac = None
    ap_id = None
    ap_name = None
    site_name = None
    event_type = None
    reason = None
    audit_id = None
    
    if "org_id" in event:
        org_id = event["org_id"]
    if "site_id" in event:
        site_id = event["site_id"]
    if "ap" in event:
        ap_mac = event["ap"]
        ap_id= "00000000-0000-0000-1000-%s" % (ap_mac)
    if "ap_name" in event:
        ap_name = event["ap_name"]
    if "site_name" in event:
        site_name = event["site_name"]
    if "type" in event:
        event_type = event["type"]
    if "reason" in event:
        reason = event["reason"]
        event_type = event["type"]
    if "audit_id" in event:
        audit_id = event["audit_id"]
    return [org_id, site_id, site_name, ap_mac, ap_id, ap_name, event_type, reason, audit_id]

def _ap_config_changed_by_rrm(ap_mac, ap_name, site_name):
    '''
20/05/2020 06:30:53 INFO: device-events
20/05/2020 06:30:53 INFO: ap: d420b0002e95
20/05/2020 06:30:53 INFO: ap_name: ap-41.off.lab
20/05/2020 06:30:53 INFO: audit_id: 6175746f-0000-0000-3157-000000000000
20/05/2020 06:30:53 INFO: org_id: 203d3d02-dbc0-4c1b-9f41-76896a3330f4
20/05/2020 06:30:53 INFO: site_id: fa018c13-008b-46ae-aa18-1eeb894a96c4
20/05/2020 06:30:53 INFO: site_name: lab
20/05/2020 06:30:53 INFO: timestamp: 1589956241
20/05/2020 06:30:53 INFO: type: AP_CONFIG_CHANGED_BY_RRM
    '''
    text = []
    text_string = "Configuration for AP \"%s\" (MAC: %s) " %(ap_name, ap_mac)
    if site_name:
        text_string += "on site \"%s\" " %(site_name)
    text_string += "is changed by RRM."
    text.append(text_string)
    return text

def _ap_config_changed_by_user(ap_mac, ap_name, site_name):
    '''
19/05/2020 07:16:11 INFO: device-events
19/05/2020 07:16:11 INFO: ap: d420b0002e95
19/05/2020 07:16:11 INFO: ap_name: ap-41.off.lab
19/05/2020 07:16:11 INFO: audit_id: b2b06f12-02f1-48d7-9682-f82766c4002c
19/05/2020 07:16:11 INFO: org_id: 203d3d02-dbc0-4c1b-9f41-76896a3330f4
19/05/2020 07:16:11 INFO: site_id: fa018c13-008b-46ae-aa18-1eeb894a96c4
19/05/2020 07:16:11 INFO: site_name: lab
19/05/2020 07:16:11 INFO: timestamp: 1589872563
19/05/2020 07:16:11 INFO: type: AP_CONFIG_CHANGED_BY_USER
    '''
    text = []
    text_string = "Configuration for AP \"%s\" (MAC: %s) " %(ap_name, ap_mac)
    if site_name:
        text_string += "on site \"%s\" " %(site_name)
    text_string += "is changed by User."
    text.append(text_string)
    return text

def _1026(ap_mac, ap_name, site_name, reason):
    '''
19/05/2020 00:21:04 INFO: device-events
19/05/2020 00:21:04 INFO: ap: d420b0002e95
19/05/2020 00:21:04 INFO: ap_name: ap-41.off.lab
19/05/2020 00:21:04 INFO: org_id: 203d3d02-dbc0-4c1b-9f41-76896a3330f4
19/05/2020 00:21:04 INFO: reason: scheduled-site-rrm
19/05/2020 00:21:04 INFO: site_id: fa018c13-008b-46ae-aa18-1eeb894a96c4
19/05/2020 00:21:04 INFO: site_name: lab
19/05/2020 00:21:04 INFO: timestamp: 1589847656
19/05/2020 00:21:04 INFO: type: 1026
    '''
    text = []
    text_string = "Event 1026 for AP \"%s\" (MAC: %s) " %(ap_name, ap_mac)
    if site_name:
        text_string += "on site \"%s\" " %(site_name)
    text_string += "because of %s." %(reason)
    text.append(text_string)    
    return text

def _ap_assigned(ap_mac, ap_name, site_name):
    '''
19/05/2020 00:21:04 INFO: device-events
19/05/2020 00:21:04 INFO: ap: d420b0002e95
19/05/2020 00:21:04 INFO: ap_name: ap-41.off.lab
19/05/2020 00:21:04 INFO: org_id: 203d3d02-dbc0-4c1b-9f41-76896a3330f4
19/05/2020 00:21:04 INFO: reason: scheduled-site-rrm
19/05/2020 00:21:04 INFO: site_id: fa018c13-008b-46ae-aa18-1eeb894a96c4
19/05/2020 00:21:04 INFO: site_name: lab
19/05/2020 00:21:04 INFO: timestamp: 1589847656
19/05/2020 00:21:04 INFO: type: 1026
    '''
    text = []
    text_string = "AP \"%s\" (MAC: %s) is assigned" %(ap_name, ap_mac)
    if site_name:
        text_string += " to site \"%s\" " %(site_name)
    text_string += "."
    text.append(text_string)    
    return text

def _ap_unassigned(ap_mac, ap_name, site_name):
    '''
20/05/2020 12:57:21 INFO: device-events
20/05/2020 12:57:21 INFO: ap: 5c5b351ef069
20/05/2020 12:57:21 INFO: ap_name: bt-11.ktc.lab
20/05/2020 12:57:21 INFO: audit_id: 38aaf359-5c60-4ed8-9c08-04a9a244e478
20/05/2020 12:57:21 INFO: org_id: 203d3d02-dbc0-4c1b-9f41-76896a3330f4
20/05/2020 12:57:21 INFO: site_id: fa018c13-008b-46ae-aa18-1eeb894a96c4
20/05/2020 12:57:21 INFO: site_name: test_only_1
20/05/2020 12:57:21 INFO: text: AP 5c5b351ef069 unassigned
20/05/2020 12:57:21 INFO: timestamp: 1589979432
20/05/2020 12:57:21 INFO: type: AP_UNASSIGNED
    '''
    text = []
    text_string = "AP \"%s\" (MAC: %s) is unassigned" %(ap_name, ap_mac)
    #if site_name:
    #    text_string += " from site %s" %(site_name)
    text_string += "."
    text.append(text_string)    
    return text


def _ap_common(ap_mac, ap_name, site_name, event_type):
    '''
20/05/2020 06:30:54 INFO: device-events
20/05/2020 06:30:54 INFO: ap: d420b0002e95
20/05/2020 06:30:54 INFO: ap_name: ap-41.off.lab
20/05/2020 06:30:54 INFO: org_id: 203d3d02-dbc0-4c1b-9f41-76896a3330f4
20/05/2020 06:30:54 INFO: site_id: fa018c13-008b-46ae-aa18-1eeb894a96c4
20/05/2020 06:30:54 INFO: site_name: lab
20/05/2020 06:30:54 INFO: timestamp: 1589956243
20/05/2020 06:30:54 INFO: type: AP_CONFIGURED
    '''
    text = []
    text_string = "AP \"%s\" (MAC: %s) " %(ap_name, ap_mac)
    if site_name:
        text_string += "on site \"%s\" " %(site_name)
    text_string += "is %s." %(event_type.replace("AP_", "").title())
    text.append(text_string)
    return text


