from datetime import datetime, timedelta
from .alarm_common import CommonAlarm
from .alarm_infra import InfraAlarm

def alarm(mist_host, alarm_channels, mist_event):

    event = None
    if "group" in mist_event:
        if mist_event["group"] == "infrastructure":
            event = InfraAlarm(mist_host, alarm_channels, mist_event)
        elif mist_event["group"] == "marvis":
            event = CommonAlarm(mist_host, alarm_channels, mist_event)
        elif mist_event["group"] == "security":
            event = CommonAlarm(mist_host, alarm_channels, mist_event)
    if not event:
        event = CommonAlarm(mist_host, alarm_channels, mist_event)

    return event.get()
