
########################
# mist_conf:
# Configuration to receive webhooks from Mist Cloud and to send API 
# requests to Mist Cloud
# 
# apitoken:             apitoken from Mist Cloud to sent API requests
# mist_cloud:           api.mist.com if you are using US Cloud, or 
#                       api.eu.mist.com if you are using EU Cloud
# server_uri:           uri where you want to receive wehbooks messages
#                       on this server. 
# site_id_ignored:      Array of site ids you want to ignore (MWTT will 
#                       discard webhooks about these sites)
mist_conf={
    "apitoken": "xxxxxxxxxxxxxxx",
    "mist_cloud": "api.mist.com",
    "server_uri": "/mist-webhooks",
    "site_id_ignored": [],
    "approved_admins": []
}
log_level = 6
########################
# slack_conf
# if the script has to send logs to slack webhook. To get the Slack 
# Webhook URL, please go to https://api.slack.com/app
# enabled:      if you want to enable Slack reporting
# url:          URL of your slack webhook
slack_conf = {    
    "enabled": True,
    "url": {
        "debug": "https://hooks.slack.com/services/XXXXXXXXX/XXXXXXXXX",
        "info": "https://hooks.slack.com/services/XXXXXXXXX/XXXXXXXXX",
        "warning": "https://hooks.slack.com/services/XXXXXXXXX/XXXXXXXXX",
        "unknown": "https://hooks.slack.com/services/XXXXXXXXX/XXXXXXXXX"
    }
}

msteams_conf = {
    "enabled": False,
    "url": {
        "warning": "https://outlook.office.com/webhook/XXXXXXXXX/IncomingWebhook/XXXXXXXXX",
        "info": "https://outlook.office.com/webhook/XXXXXXXXX/IncomingWebhook/XXXXXXXXX",
        "debug": "https://outlook.office.com/webhook/XXXXXXXXX/IncomingWebhook/XXXXXXXXX",
        "unknown": "https://outlook.office.com/webhook/XXXXXXXXX/IncomingWebhook/XXXXXXXXX"
    }
}
color_config = {
    "location":"#D5D8DC", 
    "zone":"#808B96", 
    "rssizone":"#1C2833", 
    "vbeacon":"#5D6D7E", 
    "asset-raw":"#AEB6BF", 
    "device-events":"#229954", 
    "device-updowns":"#2E86C1",
    "alarms":"#C70039", 
    "audits":"#FFC300", 
    "client-sessions":"#884EA0",
}


message_levels = {
    "audits": {
        "debug": [],
        "info": [],
        "warning": []
    },
    "device-events": {
        "debug": ["AP_CONFIG_CHANGED_BY_RRM", "1026", "AP_RECONFIGURED", "AP_RESTART_BY_USER", "AP_CONFIG_CHANGED_BY_USER"],
        "info": ["AP_CONNECTED", "AP_DISCONNECTED", "AP_RESTARTED", "AP_ASSIGNED", "AP_UNASSIGNED", "AP_CONFIGURED"],
        "warning": []
    }
}
