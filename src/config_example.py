
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
    "site_id_ignored": []
}
log_level = 6
########################
# slack_conf
# if the script has to send logs to slack webhook. To get the Slack 
# Webhook URL, please go to https://api.slack.com/app
# enabled:      if you want to enable Slack reporting
# url:          URL of your slack webhook
slack_conf = {
    "enabled" : False,
    "url": "https://hooks.slack.com/services/XXXXXXXXX/XXXXXXXXX"
}