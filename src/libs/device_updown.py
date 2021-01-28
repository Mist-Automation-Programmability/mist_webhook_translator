from datetime import datetime, timedelta

def device_updown(topic, mist_host, updown_channels, event):
    org_id = None
    site_id = None
    ap = None
    event_type = None
    text = []
    actions = []
    channel = None
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
        ap_name = event["ap_name"]
    if "site_name" in event:
        site_name = event["site_name"]
    if "reason" in event:
        reason = event["reason"]
    if "type" in event:
        event_type = event["type"]
        try:
            mod_event_type = event_type.replace("AP_","").title()        
            text.append("AP %s (MAC: %s) %s because of %s" %(ap_name, ap, mod_event_type, reason))
        except:
            text.append("AP Name: %s" %(ap_name))
            text.append("AP MAC: %s" %(ap))
            text.append("Site: %s" %(site_name))
            text.append("Event: %s" %(event_type))
            text.append("Reason: %s" %(reason))
    else:
        text.append("AP Name: %s" %(ap_name))
        text.append("AP MAC: %s" %(ap))
        text.append("Site: %s" %(site_name))
        text.append("Event: %s" %(event_type))
        text.append("Reason: %s" %(reason))


    host = mist_host.replace("api", "manage")
    url_insights= "https://%s/admin/?org_id=%s#!dashboard/insights/device/%s/24h/%s/%s/%s" % (host,org_id, ap_id, t_start, t_stop, site_id)
    actions.append({"tag": "insights", "text": "AP Insights", "url": url_insights})
    url_conf = "https://%s/admin/?org_id=%s#!ap/detail/%s/%s" %(host,org_id, ap_id, site_id)
    actions.append({"tag": "insights", "text": "AP Configuration", "url": url_conf})


    if event["type"] in updown_channels:
        channel = updown_channels[event["type"]]

    return [channel, text, actions]

