from .device_event_ap import ApEvent
from .device_event_switch import SwitchEvent
from .device_event_gateway import GatewayEvent
from .device_event_common import CommonEvent

def device_event(mist_host, message_levels, mist_event):
    event = None
    if "device_type" in mist_event:
        if mist_event["device_type"] == "ap":
            event = ApEvent(mist_host, message_levels, mist_event)            
        elif mist_event["device_type"] == "switch":
            event = SwitchEvent(
                mist_host, message_levels, mist_event)
        elif mist_event["device_type"] == "gateway":
            event = GatewayEvent(
                mist_host, message_levels, mist_event)
    if not event:
        event = CommonEvent(mist_host, message_levels, mist_event)
    
    return event.get()
