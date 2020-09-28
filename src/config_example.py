########################
# mist_conf:
# Configuration to receive webhooks from Mist Cloud and to send API
# requests to Mist Cloud
#
# apitoken:         apitoken from Mist Cloud to sent API requests
# mist_cloud:       api.mist.com if you are using US Cloud, or
#                   api.eu.mist.com if you are using EU Cloud
# server_uri:       uri where you want to receive wehbooks messages
#                   on this server.
# mist_secret:      the webhook secret configuration on the Mist Cloud
#                   to secure webhook reception
mist_conf = {
    "apitoken": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "mist_host": "manage.mist.com",
    "mist_secret": None,
    "server_uri": "/webhooks",
    "site_id_ignored": [],
    "approved_admins": ["user@domain.com"]
}
log_level = 6
slack_conf = {
    "enabled": True,
    "url": {
        "debug": "https://hooks.slack.com/services/XXXXXXXX/XXXXXXXXX/XXXXXXXXXXX1",
        "info": "https://hooks.slack.com/services/XXXXXXXX/XXXXXXXXX/XXXXXXXXXXX2",
        "warning": "https://hooks.slack.com/services/XXXXXXXX/XXXXXXXXX/XXXXXXXXXXX3",
        "unknown": "https://hooks.slack.com/services/XXXXXXXX/XXXXXXXXX/XXXXXXXXXXX4",
        "ap": "https://hooks.slack.com/services/XXXXXXXX/XXXXXXXXX/XXXXXXXXXXX4",
        "sw": "https://hooks.slack.com/services/XXXXXXXX/XXXXXXXXX/XXXXXXXXXXX4",
        "gw": "https://hooks.slack.com/services/XXXXXXXX/XXXXXXXXX/XXXXXXXXXXX4"
    }
}

msteams_conf = {
    "enabled": True,
    "url": {
        "warning": "https://outlook.office.com/webhook/xxxxxxxxxxxx/IncomingWebhook/xxxxxxxxxxx/xxxxxxxxxxx",
        "info": "https://outlook.office.com/webhook/xxxxxxxxxxxx/IncomingWebhook/xxxxxxxxxxx/xxxxxxxxxxx",
        "debug": "https://outlook.office.com/webhook/xxxxxxxxxxxx/IncomingWebhook/xxxxxxxxxxx/xxxxxxxxxxx",
        "unknown": "https://outlook.office.com/webhook/xxxxxxxxxxxx/IncomingWebhook/xxxxxxxxxxx/xxxxxxxxxxx"
    }
}

color_config = {
    "location": "#D5D8DC",
    "zone": "#808B96",
    "rssizone": "#1C2833",
    "vbeacon": "#5D6D7E",
    "asset-raw": "#AEB6BF",
    "device-events": "#229954",
    "device-updowns": "#2E86C1",
    "alarms": "#C70039",
    "audits": "#FFC300",
    "client-sessions": "#884EA0",
}

#Only apply to device_events and device_updowns
message_levels = {
    "debug": [
        "CONFIG_CHANGED_BY_RRM",
        "1026",
        "RECONFIGURED",
        "RESTART_BY_USER",
        "CONFIG_CHANGED_BY_USER",
        "AP_ASSIGNED",
        "AP_UNASSIGNED",
        "GW_ASSIGNED",
        "GW_UNASSIGNED",
        "SW_ASSIGNED",
        "SW_UNASSIGNED"
    ],
    "info": [
        "AP_CONNECTED",
        "AP_DISCONNECTED",
        "AP_RESTARTED",
        "AP_CONFIGURED",
        "GW__CONFIGURED",
        "SW_RESTARTED",
        "SW_CONFIGURED",
        "SW_PORT_UP",
        "SW_PORT_DOWN"
    ],
    "warning": [
        "DISCONNECTED_LONG",
        "SW_CONNECTED",
        "SW_DISCONNECTED",
        "GW_CONNECTED",
        "GW_DISCONNECTED",
        "GW_RESTARTED"
    ]
}