# Mist Want To Talk
MWTT is a small python app to publish Mist Webhook messages to Slack or MsTeams channels.

It is composed of lightweight python web server ([Flask](https://github.com/pallets/flask)) and python code to process the webhook information and send it the Slack/MsTeams channels.

This script is available as is and can be run on any server with Python3. 

The script is also available as a Docker image. It is designed to simplify the deployment, and a script is available to automate the required images deployment.

## MIT LICENSE
 
Copyright (c) 2021 Thomas Munzer

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the  Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# IMPORTANT
To get this script working, you will have to manually configure webhooks on your Mist account and enable the "audits", "alarms, "device-events" and/or "device-updowns" topics. This configuration can be done at the Organization level, or at the site level, depending on your needs.
For some topics, if they are enable at the Org and Site(s) levels, you may receive the same message multiple times.

This will tell Mist Cloud to send events (like AP Connected/Disconnected) to the MWTT FQDN. As of today (January, 2020), some topics like the "device-events" topics cannot be enabled directly from the Mist UI. This configuration can be done through Mist APIs. You can use the web UI to manage APIs by reaching https://api.mist.com/api/v1/orgs/:your_org_id/webhooks or https://api.eu.mist.com/api/v1/orgs/:your_org_id/webhooks (Be sure to replace ":your_org_id" first). Then you will be able to create a new webhook by using the following settings:

`
    {
        "url": "https://<mwtt_server_fqdn>/<mwtt_url>",
        "topics": [
            "device-events"
        ],
        "enabled": true
    }
   `


# features:
* Send the messages to different slack channels depending on the severity level (can be configured):
<img src="https://github.com/tmunzer/mwtt/raw/master/._readme/img/slack.png" width="50%">

* Send the messages to different MS Teams channels depending on the severity level (can be configured):
<img src="https://github.com/tmunzer/mwtt/raw/master/._readme/img/msteams.png" width="50%">

# How to use it
## Docker Image
You can easily deploy this application as a [Docker](https://www.docker.com/) image. The image is publicly available on Docker Hub at https://hub.docker.com/r/tmunzer/mwtt/.
In this case, you can choose to manually deploy the image and create the container, or you can use the automation script (for Linux).

If you want to manually deploy the Docker image, the Mwtt container will listen for HTTP messages on port `TCP51361`
### Automation Script
The Automation script will allow you to easily 
* Create the application permanent folder and generate a config file
* Manage HTTPS certificates with self-signed certificates 
* Download, Deploy, Update the application container
To use this script, just download it [here](https://raw.githubusercontent.com/tmunzer/mwtt/master/mwtt.sh), and run it in a terminal.


When you are starting the script for the first time, it will ask some question:
##### Application FQDN
This parameter is very important, and the value must be resolvable by the HTTP clients. The script is deploying a NGINX containter in front of the application container. NGINX will be in charge to manage HTTPS connections, and to route the HTTP/HTTPS traffic to the right application (it is build to allow to run different applications on the same server). This routing is done based on the `host` parameter in the HTTP headers.

##### Permanent Folder
The script will automatically create a folder in the permanent folder you configured. This folder will be used to store permanent data from the application. The script will also generate a `config.py` file containing configuration example and help.

## Docker-Compose
You can find a docker-compose.yaml file in the root folder of the repository. This file can be used to quickly deploy the app without using the automation script.
Please note, in this case, you will have to manually generate all the required configuration files!

## Configuration
### MWTT Configuration
Before starting the MWTT application, you will have to configure it. To do so, edit the file `config.py` located in the folder permananent_folder/mwtt created by the deployment script.

The file `config.py` already contains the configuration structure with example values. 

If you want to manually create this file, you can check the `src/config_example.py` file to see the required variables.

## Usage
### Start/Stop the MWTT Application
This can be done through the deployment script, or directly by using Docker commands. If you do it manually, you will have to start/stop both containers, `jwilder/nginx-proxy` and `tmunzer/mwtt`.
### Docker Tips
Depending on your system and your settings, you may have to add `sudo` in front of the following commands
- `docker ps`: list all you docker containers currently running. This command will also show you the container id.
- `docker ps -a`: list all you docker containers. This command will also show you the container id.
- `docker start <container_id>`: manually start a docker container.
- `docker stop <container_id>`: manually stop a docker container.
- `docker logs <container_id>`: show the container logs
- `docker logs -f <container_id>`: continuously show the container logs

