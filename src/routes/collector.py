from curses import can_change_color
import json
import bson.json_util as json_util
from mwtt.src import mwtt
from mwtt import Console
from datetime import datetime

console = Console("wh_collector")


def whCollectorPost(request, org_id, db):
    console.info(" New message reveived ".center(60, "-"))
    console.info(f"Org id:  {org_id} ")

    start = datetime.now()
    try:
        settings = db["settings"].find_one({"org_id": org_id})
        settings = json.loads(json_util.dumps(settings))
        console.debug(f"settings loaded from DB for org {org_id}")
    except:
        console.error(f"unable to load settings from DB for org {org_id}")
        return "", 500
    channels = {}
    channels_count = 0
    for topic in settings["topics_status"]:
        if settings["topics_status"][topic]:
            channels[topic]=settings["topics"][topic]
            channels_count += 1
            
    if channels_count:
        res = mwtt.new_event(
            request,
            settings["mist_settings"],
            channels,
            settings["slack_settings"],
            settings["teams_settings"]
        )
    else:
        res = "", 200
    delta = datetime.now() - start
    console.info(f"Processing time {delta.seconds}.{delta.microseconds}s")
    return res
