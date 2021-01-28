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
    "default_url": "https://hooks.slack.com/services/XXXXXXXX/XXXXXXXXX/XXXXXXXXXXX4",
    "url": {
        "debug": "https://hooks.slack.com/services/XXXXXXXX/XXXXXXXXX/XXXXXXXXXXX1",
        "info": "https://hooks.slack.com/services/XXXXXXXX/XXXXXXXXX/XXXXXXXXXXX2",
        "warning": "https://hooks.slack.com/services/XXXXXXXX/XXXXXXXXX/XXXXXXXXXXX3"
    }
}

msteams_conf = {
    "enabled": True,
    "default_url": "https://outlook.office.com/webhook/xxxxxxxxxxxx/IncomingWebhook/xxxxxxxxxxx/xxxxxxxxxxx",
    "url": {
        "warning": "https://outlook.office.com/webhook/xxxxxxxxxxxx/IncomingWebhook/xxxxxxxxxxx/xxxxxxxxxxx",
        "info": "https://outlook.office.com/webhook/xxxxxxxxxxxx/IncomingWebhook/xxxxxxxxxxx/xxxxxxxxxxx",
        "debug": "https://outlook.office.com/webhook/xxxxxxxxxxxx/IncomingWebhook/xxxxxxxxxxx/xxxxxxxxxxx"
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

# Only apply to device_events and device_updowns
event_channels = {
    "AP_UNCLAIMED": "warning",
    "AP_CLAIMED": "warning",
    "AP_ASSIGNED": "info",
    "AP_UNASSIGNED": "info",
    "AP_CONFIG_CHANGED_BY_RRM": "debug",
    "AP_CONFIG_CHANGED_BY_USER": "info",
    "AP_RECONFIGURED": "debug",
    "1026": "debug",
    "AP_RESTART_BY_USER": "info",
    "AP_CONNECTED": "info",
    "AP_DISCONNECTED": "info",
    "AP_RESTARTED": "info",
    "AP_CONFIGURED": "debug",
    "AP_DISCONNECTED_LONG": "warning",
    "AP_UPGRADE_BY_USER": "info",
    "AP_UPGRADED": "debug",

    "GW_UNCLAIMED": "warning",
    "GW_CLAIMED": "warning",
    "GW_ASSIGNED": "info",
    "GW_UNASSIGNED": "info",
    "GW_CONFIG_CHANGED_BY_USER": "info",
    "GW_RECONFIGURED": "debug",
    "GW_CONFIGURED": "debug",
    "GW_CONFIG_FAILED": "warning",
    "GW_PORT_UP": "info",
    "GW_PORT_DOWN": "info",
    "GW_CONNECTED": "info",
    "GW_DISCONNECTED": "info",
    "GW_RESTARTED": "info",
    "GW_DISCONNECTED_LONG": "warning",
    "GW_OSPF_UP_NEIGHBOR_UP": "debug",
    "GW_OSPF_NEIGHBOR_DOWN": "debug",

    "SW_UNCLAIMED": "warning",
    "SW_CLAIMED": "warning",
    "SW_ASSIGNED": "info",
    "SW_UNASSIGNED": "info",
    "SW_CONFIG_CHANGED_BY_USER": "info",
    "SW_DYNAMIC_PORT_ASSIGNED": "info",
    "SW_CONFIGURED": "debug",
    "SW_RECONFIGURED": "debug",
    "SW_CONFIG_FAILED": "warning",
    "SW_ZTP_FINISHED": "info",
    "SW_PORT_UP": "debug",
    "SW_PORT_DOWN": "debug",
    "SW_CONNECTED": "info",
    "SW_DISCONNECTED": "info",
    "SW_RESTARTED": "info",
    'SW_GET_SUPPORT_FILES': "info",
    'SW_HANDSHAKE_ERROR': "warning",
    'SW_PORT_STORM_CONTROL': "warning",
    'SW_REASSIGNED': "debug",
    'SW_REJECTED': "warning",
    'SW_RESTART_BY_USER': "info",
    'SW_STP_TOPO_CHANGED': "info",
    'SW_VC_BACKUP_ELECTED': "warning",
    'SW_VC_MASTER_CHANGED': "warning",
    'SW_VC_MEMBER_ADDED': "info",
    'SW_VC_MEMBER_DELETED': "warning"

}

updown_channels = {
    "AP_CONNECTED": "info",
    "AP_DISCONNECTED": "info",
    "AP_RESTARTED": "info",
    "GW_CONNECTED": "info",
    "GW_DISCONNECTED": "info",
    "GW_RESTARTED": "info",
    "SW_CONNECTED": "info",
    "SW_DISCONNECTED": "info",
    "SW_RESTARTED": "info"
}

alarm_channels = {
    "device_down": "info",
    "device_restarted": "info",
    "gateway_down": "warning",
    "gateway_restarted": "warning",
    "switch_down": "warning",
    "switch_restarted": "warning"
}
