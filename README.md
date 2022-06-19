# Mist Webhook Translator
Mist Webhook Translator is a python web app to publish Mist Webhook messages to Slack or MsTeams channels.

<img src="https://github.com/tmunzer/mist_webhook_translator/raw/main/._readme/img/archi.png" width="75%">

It is providing a Web UI to configure the App, and is automatically configuring the Webhook in Mist and listening for incoming webhooks.
From there, it is processing the messages and forward them to Slack / Teams based on the configuration.

This app is using [mwtt](https://github.com/tmunzer/mwtt) to process the webhooks. You can use mwtt directly if you don't need the Web UI

The script is also available as a Docker image. It is designed to simplify the deployment, and a script is available to automate the required images deployment.


# Menu
* [License](#mit-license)
* [Features](#features)
* [Installation](#installation)


# MIT LICENSE
 
Copyright (c) 2022 Thomas Munzer

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the  Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Features
* Provides Web UI for configuration (Mist webhook topics, Slack/Teams incoming webhooks)
<img src="https://github.com/tmunzer/mist_webhook_translator/raw/main/._readme/img/config.jpg" width="50%">
* Automatically create and delete Webhook configuration in Mist Org (based on the required settings)
* Automatically set the Mist Webhook Secret and check the `X-Signature-v2` header in the message
* Listen for Webhook messages comming from Mist Cloud
* Send the messages to different slack channels depending on the severity level (can be configured):
<img src="https://github.com/tmunzer/mist_webhook_translator/raw/main/._readme/img/slack_channel.png" width="50%">
* Send the messages to different MS Teams channels depending on the severity level (can be configured):
<img src="https://github.com/tmunzer/mist_webhook_translator/raw/main/._readme/img/msteams_channel.png" width="50%">

### Supported Webhook Topics
* alarms
* audits
* device-updowns
* device-events
* mxedge-events

# Installation
This Reference Application can be used as a standalone Application, or it can be deployed as a Docker Image (recommanded).

## Deploy the Docker version (recommanded)
This application is available as a [Docker Image](https://hub.docker.com/repository/docker/tmunzer/mist_webhook_translator). The Dockerfile is also available if you want top build it on your own.


The Docker Image exposes the following ports:
* TCP51361


### Run the Docker version
`   docker create -v  <path_to_env_file>:/app/.env:ro --name="<container_name>" -p 51361:80 tmunzer/mist_webhook_translator`

### Configure the Docker version
Configuration can be done through the environment files/variables. An example of configuration can be found in `src/env`. Edit it to match your settings and link the `env` file to `/app/.env` in you container, or use the environment variables

You can also use environment variables to configure the app:

Variable Name | Type | Default Value | Comment 
------------- | ---- | ------------- | ------- 
FLASK_SECRET | string |  | Used to sign the session cookies. Can be generated with the command `python -c 'import secrets; print(secrets.token_hex())'` |
FLASK_DEBUG | boolean | False | Turn debug mode on, allowing to get more logs and error details from the app. Do NOT use it in production |
FLASK_PORT | integer | 51361 | TCP Port used by Flask to listen to HTTP requests. Do NOT change it if using the Docker version (the image is only exposing TCP51361) |
WH_HOST | string |  | FQDN used to configure the Mist Webhooks. Mist Cloud must be able to reach this FQDN |
WH_HTTPS | boolean | False | Used to configure the Mist Webhooks to send HTTP POST through HTTPS (True) or HTTP (False). If `True`, a reverse proxy must be deployed in front of the App to manage HTTPS.
WH_PORT | integer | 51361 | Port to configure the Mist Webhooks. Mist Cloud must be able to send HTTP POST on this port. By default it is the same as FLASK_PORT, but can be changed when using a reverse proxy in front of the app |
MONGO_USER | string | null | If the Mongo server require authentication |
MONGO_PASSWORD | string | null | If the Mongo server require authentication |
MONGO_HOST | string | null | Mongo server hostname |
MONGO_PORT | integer | 27017 | Mongo server port |
MONGO_DB | string | translator | Mongo Database name |
MONGO_KEY | string |  | Used to encrypt data in the DB. Can be generated with `python -c 'import secrets; print(secrets.token_hex(16))'` |
ABOUT_TOKEN | string | secret_token | used to "hide" server status URL. The URL `/status/about/<string:token>` is exposing some basic status info about this app |


## Deploy the Standalone Application
This Reference APP is built over Python Flask. 

### Deploy the Application
* Install Python.
* Clone this repo.
* Configure the APP settings, in the `src/.env` file. You will find an example in `src/env`. With Docker deployment, all the settings can be configured by using Environment Variables (see above)
* Install python packages (`python3 -m pip install -r requirements.txt` from the project folder).
* Start the APP with `python3 ./app.py` from the `src` folder


