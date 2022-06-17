import json
from signal import alarm
from topics import topics, topic_names



def check_alarms(current_alarms):
    print()
    print(" ALARMS ".center(80, "-"))
    new_alarms = []
    with open("./alarm_defs.json", "r") as f:
        alarms = json.loads(f.read())
        for alarm in alarms:
            if alarm["key"] not in current_alarms:
                new_alarm =     {"topic": "alarms", "sub_topic": alarm["group"], "name": alarm["key"], "channel": alarm["severity"]}
                print(f"{new_alarm},")
                new_alarms.append(new_alarm)
    return new_alarms

def check_events(event_type, current_events):
    print()
    print(f" {event_type.upper()} EVENTS ".center(80, "-"))
    new_events = []
    with open(f"./{event_type}_events.json", "r") as f:
        events = json.loads(f.read())
        for event in events:
            if event["key"] not in current_events:
                new_event =     {"topic": f"{event_type}-events", "sub_topic": "", "name": event["key"], "channel": ""}
                print(f"{new_event},")
                new_events.append(new_event)
    return new_events

if __name__ == "__main__":
    current_data = {}
    new_data = {}
    for tname in topic_names:
        current_data[tname] = []
        new_data[tname] = []
    for topic in topics:
        current_data[topic["topic"]].append(topic["name"])
        
    new_data["alarms"] = check_alarms(current_data["alarms"])
    new_data["device-events"] = check_events("device", current_data["device-events"])
    new_data["mxedge-events"] = check_events("mxedge", current_data["mxedge-events"])
    print()
    print("".center(80, "-"))
    print()
    for topic in new_data:
        print()
        print(f" {topic.upper()} ".center(80, "-"))
        for entry in new_data[topic]:
            print(f'"{entry["name"]}": "{entry["channel"]}",')