from .device_event_common import CommonEvent


class MEEvent(CommonEvent):

    def __init__(self, mist_host, message_levels, event):
        CommonEvent.__init__(self, mist_host, message_levels, event)


    def _process(self):
        if self.event_type in ["ME_CLAIMED", "ME_UNCLAIMED"]:
            self._claimed()
        elif self.event_type == "ME_ASSIGNED":
            self._assigned()
        elif self.event_type == "ME_UNASSIGNED":
            self._unassigned()
        else:
            self._common()

