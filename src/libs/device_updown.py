from datetime import datetime, timedelta


def device_updown(mist_host, updown_channels, event):

    mist_dashboard = mist_host.replace("api", "manage")
    org_id = event.get("org_id", None)
    site_id = event.get("site_id", None)
    site_name = event.get("site_name", None)
    device_type = event.get("device_type", None)
    device_name = event.get("device_name", None)
    device_mac = event.get("mac", None)
    if device_mac:
        device_id = f"00000000-0000-0000-1000-{device_mac}"
    event_type = event.get("type", None)
    reason = event.get("reason", None)

    subtitle = ""
    text = []
    actions = []
    channel = None

    d_stop = datetime.now()
    d_start = d_stop - timedelta(days=1)
    t_stop = int(datetime.timestamp(d_stop))
    t_start = int(datetime.timestamp(d_start))

    text.append(f"*Device* : {device_name} ({device_id})")
    text.append(f"*Event*  : {event_type}")
    if reason:
        text.append(f"*Reason*: {reason}")

    subtitle = f"{event_type.split('_')[0]} {device_name} (MAC: {device_mac}) {event_type}"

    url_insights = f"https://{mist_dashboard}/admin/?org_id={org_id}#!dashboard/insights/device/{device_id}/24h/{t_start}/{t_stop}/{site_id}"
    actions.append(
        {"tag": "insights", "text": "AP Insights", "url": url_insights})
    url_conf = f"https://{mist_dashboard}/admin/?org_id={org_id}#!ap/detail/{device_id}/{site_id}"
    actions.append(
        {"tag": "insights", "text": "AP Configuration", "url": url_conf})

    if event["type"] in updown_channels:
        channel = updown_channels[event["type"]]

    return [channel, subtitle, text, actions]
