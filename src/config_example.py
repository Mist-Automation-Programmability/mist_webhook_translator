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
# You can create more slack / msteams channel urls depending on your needs, you just need to be sure each
# channel has a unique name
slack_conf = {
    "enabled": True,
    "default_url": "https://hooks.slack.com/services/XXXXXXXX/XXXXXXXXX/XXXXXXXXXXX4",
    "url": {
        "debug": "https://hooks.slack.com/services/XXXXXXXX/XXXXXXXXX/XXXXXXXXXXX1",
        "info": "https://hooks.slack.com/services/XXXXXXXX/XXXXXXXXX/XXXXXXXXXXX2",
        "warning": "https://hooks.slack.com/services/XXXXXXXX/XXXXXXXXX/XXXXXXXXXXX3",
        "critical": "https://hooks.slack.com/services/XXXXXXXX/XXXXXXXXX/XXXXXXXXXXX3",
    }
}

msteams_conf = {
    "enabled": True,
    "default_url": "https://outlook.office.com/webhook/xxxxxxxxxxxx/IncomingWebhook/xxxxxxxxxxx/xxxxxxxxxxx",
    "url": {
        "debug": "https://outlook.office.com/webhook/xxxxxxxxxxxx/IncomingWebhook/xxxxxxxxxxx/xxxxxxxxxxx",
        "info": "https://outlook.office.com/webhook/xxxxxxxxxxxx/IncomingWebhook/xxxxxxxxxxx/xxxxxxxxxxx",
        "warning": "https://outlook.office.com/webhook/xxxxxxxxxxxx/IncomingWebhook/xxxxxxxxxxx/xxxxxxxxxxx",
        "critical": "https://outlook.office.com/webhook/xxxxxxxxxxxx/IncomingWebhook/xxxxxxxxxxx/xxxxxxxxxxx"
    }
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
    "GW_VPN_PATH_DOWN": "debug",
    "GW_VPN_PATH_UP": "debug",
    "GW_CERT_REGENERATED": "debug",
    "GW_DHCP_RESOLVED": "debug",
    "GW_ALARM": "warning",

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
    'SW_VC_MEMBER_DELETED': "warning",
    'SW_SYSTEM_SERVICE_RESTART': "warning"

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
    # infrastructure
    "device_down": "warning",
    "device_restarted": "info",
    "switch_down": "warning",
    "switch_restarted": "info",
    "gateway_down": "warning",
    "device_reconnected": "info",
    "switch_reconnected": "info",
    "gateway_reconnected": "info",
    "vpn_peer_down": "warning",
    "vc_master_changed": "critical",
    "vc_backup_failed": "critical",
    "vc_member_added": "info",
    "vc_member_deleted": "critical",
    "sw_alarm_chassis_poe": "warning",
    "sw_alarm_chassis_pem": "warning",
    "sw_alarm_chassis_psu": "warning",
    "sw_alarm_chassis_partition": "warning",
    "sw_dhcp_pool_exhausted": "warning",
    "gw_dhcp_pool_exhausted": "warning",
    "sw_bgp_neighbor_state_changed": "info",
    "sw_bad_optics": "warning",
    "sw_bpdu_error": "warning",
    # security
    "secpolicy_violation": "warning",
    "bssid_spoofing": "info",
    "honeypot_ssid": "info",
    "adhoc_network": "warning",
    "rogue_ap": "critical",
    "rogue_client": "critical",
    "watched_station": "warning",
    "eap_handshake_flood": "info",
    "air_magnet_scan": "info",
    "excessive_eapol_start": "warning",
    "eapol_logoff_attack": "warning",
    "eap_dictionary_attack": "warning",
    "disassociation_flood": "warning",
    "beacon_flood": "warning",
    "essid_jack": "warning",
    "krack_attack": "warning",
    "vendor_ie_missing": "warning",
    "tkip_icv_attack": "warning",
    "repeated_auth_failures": "info",
    "eap_failure_injection": "warning",
    "eap_spoofed_success": "warning",
    "out_of_sequence": "warning",
    "zero_ssid_association": "warning",
    "monkey_jack": "warning",
    "excessive_client": "warning",
    "ssid_injection": "warning",
    # marvis
    "missing_vlan": "critical",
    "bad_cable": "critical",
    "port_flap": "warning",
    "gw_bad_cable": "critical",
    "authentication_failure": "critical",
    "dhcp_failure": "critical",
    "arp_failure": "critical",
    "dns_failure": "critical",
    "negotiation_mismatch": "critical",
    "gw_negotiation_mismatch": "critical",
    "ap_offline": "warning",
    "non_compliant": "warning",
    "ap_bad_cable": "critical",
    "health_check_failed": "warning",
}
