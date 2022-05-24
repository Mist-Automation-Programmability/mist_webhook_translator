from datetime import datetime, timedelta
from .logger import Console


def device_updown(mist_host, updown_channels, event):
    console = Console("updown")

    mist_dashboard = mist_host.replace("api", "manage")
    org_id = event.get("org_id", None)
    site_id = event.get("site_id", None)
    site_name = event.get("site_name", None)
    device_type = event.get("device_type", None)
    device_name = event.get("device_name", None)
    device_mac = event.get("mac", None)
    if device_mac:
        device_id = f"00000000-0000-0000-1000-{device_mac}"
    else:
        device_id = ""
    event_type = event.get("type", None)
    reason = event.get("reason", None)

    text = ""
    info = []
    actions = []
    channel = None

    d_stop = datetime.now()
    d_start = d_stop - timedelta(days=1)
    t_stop = int(datetime.timestamp(d_stop))
    t_start = int(datetime.timestamp(d_start))

    info.append(f"*Device* : {device_name} ({device_mac})")
    info.append(f"*Event*  : {event_type}")
    if reason:
        info.append(f"*Reason*: {reason}")

    if site_name:
        text = f"Event on site {site_name}: "
    text += f"{event_type.split('_')[0]} {device_name} (MAC: {device_mac}) {event_type.split('_')[1]}"

    if device_id:
        url_insights = f"https://{mist_dashboard}/admin/?org_id={org_id}#!dashboard/insights/device/{device_id}/24h/{t_start}/{t_stop}/{site_id}"
        actions.append(
            {"tag": "insights", "text": "AP Insights", "url": url_insights})
        url_conf = f"https://{mist_dashboard}/admin/?org_id={org_id}#!ap/detail/{device_id}/{site_id}"
        actions.append(
            {"tag": "insights", "text": "AP Configuration", "url": url_conf})

    if event["type"] in updown_channels:
        channel = updown_channels[event["type"]]

    data = {
        "channel": channel,
        "title": "DEVICE UPDOWN",
        "text": text,
        "info": info,
        "actions": actions
    }
    #text = [f"Admin: {admin} (IP: {src_ip})", f"Action: {message}"]
    console.info("Processing done")
    console.debug(f"Result: {data}")
    return data
