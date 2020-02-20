#!/bin/bash

# =========================================================
# =========================================================
#
#            APP CONTAINER CREATION
#            SPECIFIC TO EACH APP
#            !!! DO NOT CHANGE !!!
#
# =========================================================
# =========================================================

function create_app_container
{
  if [ `$DOCKER ps -a | grep $APP_NAME | wc -l` -eq 0 ]
  then
    echo -e "${INFOC}INFO${NC}: $APP_NAME container not present. Creating it..."
    $DOCKER create \
    --security-opt label:disable \
    -v $PERSISTANT_FOLDER/$APP_NAME/config.py:/app/config.py:ro \
    --name="$APP_NAME" \
    --restart="on-failure:5" \
    --memory=128m \
    -e "VIRTUAL_HOST=$NODEJS_VHOST" \
    $APP_IMG
    if [ $? -eq 0 ]
    then
      echo -e "${INFOC}INFO${NC}: $APP_NAME container is now created."
    else
      echo -e "${ERRORC}ERROR${NC}: $APP_NAME container can't be created."
    fi
  else
    echo -e "${INFOC}INFO${NC}: $APP_NAME image is already created."
  fi
}

# =========================================================
# =========================================================
#
#            SYSTEM PARAMETERS
#            DO NOT CHANGE!!!
#
# =========================================================
# =========================================================
SCRIPT_CONF=`pwd`"/mwtt.conf"
SCRIPT_NAME="mwtt.py"

APP_NAME="mwtt"
APP_IMG="tmunzer/mwtt"

# =========================================================
# NGINX server configuration
# true if email server is needed by the App

NGINX_CERTS_FOLDER="certs"
NGINX_NAME="mist-proxy"
NGINX_IMG="jwilder/nginx-proxy"


DOCKER=""

# =========================================================
# Colors
INFOC='\033[0;32m'
WARNINGC='\033[0;33m'
ERRORC='\033[0;31m'
NC='\033[0m' # No Color

################################################################################
############################    BANNER
################################################################################
function banner
{
  echo ""
  echo "||============================================================================="
  echo "||"
  echo "||       $1"
  echo "||"
  echo "||============================================================================="
}

################################################################################
############################    SCRIPT CONF
################################################################################

function script_conf
{
  # FOLDER PARAMETERS
  echo "We will need a persistant folder to store application configuration, data and certificates."
  echo "Where do you want to store these data? [$PERSISTANT_FOLDER]"
  echo ""
  response=""
  while ! echo $response | grep -i "y" > /dev/null
  do
    read -p "PERSISTANT FOLDER: " PERSISTANT_FOLDER
    if ! echo $PERSISTANT_FOLDER | grep ^"/" > /dev/null
    then
      echo -e "${WARNINGC}WARNING${NC}: Incorrect input"
    else
      read -p "Is \"$PERSISTANT_FOLDER\" correct (y/n)? " response
    fi
  done
  while [ ! -d "$PERSISTANT_FOLDER" ]
  do
    echo "$PERSISTANT_FOLDER does not exist."
    create=""
    while ! echo $create | grep -i "[ny]" > /dev/null
    do
      read -p "Do you want to create it (y/n)? " create
      case $create in
        "y"|"Y") mkdir -p "$PERSISTANT_FOLDER/$APP_NAME";;
        *) exit 0;;
      esac
    done
  done
  # VHOST PARAMETER
  echo ""
  echo ""

  # SAVING PARAMETERS
  if [ -f $SCRIPT_CONF ]
  then
    mv $SCRIPT_CONF $SCRIPT_CONF.bak
  fi
  touch $SCRIPT_CONF
  while read line
  do
    if echo "$line" | grep "VHOST" > /dev/null
    then
      echo "$line" >> $SCRIPT_CONF
    fi
  done < $SCRIPT_CONF.bak
  echo "" >> $SCRIPT_CONF
  echo "PERSISTANT_FOLDER=$PERSISTANT_FOLDER" >> $SCRIPT_CONF
  echo "" >> $SCRIPT_CONF


}

function update_vhost
{
  echo "To use the NGINX reverse proxy, we will need a dedicated DNS entry for the application."
  echo "Web browsers will access the application interface from this FQDN."
  response=""
  while ! echo $response | grep -i "y" > /dev/null
  do
    read -p "Application DNS name: " NODEJS_VHOST
    read -p "Are you sure (y/n)? " response
  done
  echo "$APP_NAME-NODEJS_VHOST=$NODEJS_VHOST" >> $SCRIPT_CONF
  echo "" >> $SCRIPT_CONF
}

function init_script_conf
{
  if [ ! -f "$SCRIPT_CONF" ]
  then
    echo "-----=============-----"
    echo "--=== SCRIPT INIT ===--"
    echo ""
    echo "Before starting, here are some questions..."
    echo ""
    script_conf
    response=""
    while ! echo $response | grep -i "[y]" > /dev/null
    do
      echo ""
      echo "Current parameters:"
      echo ""
      cat $SCRIPT_CONF
      read -p "Is the configuration correct (y/n)? " response
      case $response in
        "n"|"N") script_conf;;
      esac
    done
  else
    while read line
    do
      if echo $line | grep "PERSISTANT_FOLDER" > /dev/null
      then
        PERSISTANT_FOLDER=`echo "$line" | cut -d"=" -f2`
      fi
      if echo $line | grep "$APP_NAME-NODEJS_VHOST" > /dev/null
      then
        NODEJS_VHOST=`echo "$line" | cut -d"=" -f2`
      fi
    done < $SCRIPT_CONF
  fi
  if echo "$PERSISTANT_FOLDER" | grep -i [a-z] > /dev/null
  then
    NGINX_CERTS_FOLDER="$PERSISTANT_FOLDER/$NGINX_CERTS_FOLDER"
    echo -e "${INFOC}INFO${NC}: Script configuration loaded succesfully."
  else
    echo -e "${ERRORC}ERROR${NC}: not able to load Script configuration. Exiting..."
    exit 254
  fi
  if [ ! "$NODEJS_VHOST" ]
  then
    update_vhost    
  fi
}

function read_script_conf
{
  if [ ! -f $SCRIPT_CONF ]
  then
    echo -e "${WARNINGC}WARNING${NC}: Script configuration file does not exists..."
    script_conf
  fi
  echo ""
  echo "Current parameters:"
  echo ""
  cat $SCRIPT_CONF
}

function menu_script
{
  response=""
  while ! echo $response | grep -i "[b]" > /dev/null
  do
    echo ""
    echo "1) Change Script parameters"
    echo "2) View Script parameters"
    echo "b) Back"
    echo "Please make a choice"
    read response
    case $response in
      "1") script_conf;;
      "2") read_script_conf;;
      "b") menu_main;;
    esac
  done
}


################################################################################
############################    FOLDERS
################################################################################

function check_folder # $name $FOLDER_NAME
{
  if [ ! -d $2 ]
  then
    echo -e "${INFOC}INFO${NC}: $1 folder $2 doesn't exist. Creating it..."
    mkdir -p $2
    if [ $? -eq 0 ]
    then
      echo -e "${INFOC}INFO${NC}: $1 folder $2 created."
    else
      echo ""
      echo -e "${ERRORC}ERROR${NC}: Unable to create $1 folder $2."
    fi
  else
    echo -e "${INFOC}INFO${NC}: $1 folder already exists."
  fi
}

################################################################################
############################    CERTIFICATES
################################################################################

function check_certificates
{
    if [ `ls $NGINX_CERTS_FOLDER | grep $NODEJS_VHOST.key | wc -l` -eq 0 ] || [ `ls $NGINX_CERTS_FOLDER | grep $NODEJS_VHOST.crt | wc -l` -eq 0 ]
    then
        echo -e "${INFOC}INFO${NC}: Certificates for $NODEJS_VHOST doesn't exist."
        echo "     Creating a self-signed certificate..."
        openssl req -x509 -sha256 -nodes -days 365 -newkey rsa:2048 -keyout $NGINX_CERTS_FOLDER/$NODEJS_VHOST.key -out $NGINX_CERTS_FOLDER/$NODEJS_VHOST.crt
        echo -e "${INFOC}INFO${NC}: Certificate for $NODEJS_VHOST created."
    else
        echo -e "${INFOC}INFO${NC}: Certificate for $NODEJS_VHOST already exists."
    fi
}

function new_certificate
{
    if [ -f "$NGINX_CERTS_FOLDER/$NODEJS_VHOST.crt" ]
    then
      echo -e "${INFOC}INFO${NC}: removing $NGINX_CERTS_FOLDER/$NODEJS_VHOST.crt"
      rm $NGINX_CERTS_FOLDER/$NODEJS_VHOST.crt
    fi
    if [ -f "$NGINX_CERTS_FOLDER/$NODEJS_VHOST.key" ]
    then
      echo -e "${INFOC}INFO${NC}: removing $NGINX_CERTS_FOLDER/$NODEJS_VHOST.key"
      rm $NGINX_CERTS_FOLDER/$NODEJS_VHOST.key
    fi
    openssl req -x509 -sha256 -nodes -days 365 -newkey rsa:2048 -keyout $NGINX_CERTS_FOLDER/$NODEJS_VHOST.key -out $NGINX_CERTS_FOLDER/$NODEJS_VHOST.crt
    echo -e "${INFOC}INFO${NC}: Certificate for $NODEJS_VHOST created."
  
}

function new_csr
{
  openssl req -out $NGINX_CERTS_FOLDER/$NODEJS_VHOST.csr -new -newkey rsa:2048 -nodes -keyout $NGINX_CERTS_FOLDER/$NODEJS_VHOST.key
  echo -e "${INFOC}INFO${NC}: new CSR generated. The CSR $NODEJS_VHOST.csr can be found in the folder $NGINX_CERTS_FOLDER"
  echo -e "${WARNINGC}WARNING${NC}: To be able to use the application, you will have to sign the CSR with"
  echo "         your Certificate Authority."
  echo "         The signed certificate has to be place into the folder"
  echo "         $NGINX_CERTS_FOLDER with the name $NODEJS_VHOST.crt"
}

function help_certificate
{
  echo -e "${INFOC}INFO${NC}: You can replace the self-signed certicate with your own certicate."
  echo "      To do so, you will have to generate a signed certificate on your own,"
  echo "      and to place the certificate and its private key into the folder"
  echo "      $NGINX_CERTS_FOLDER"
  echo "      The certificate has to be a X509 certificate in PEM format."
  echo "      At the end, you should have:"
  echo "      $NGINX_CERTS_FOLDER/$NODEJS_VHOST.crt"
  echo "      $NGINX_CERTS_FOLDER/$NODEJS_VHOST.key"
}

function read_certificate
{
  openssl x509 -in $NGINX_CERTS_FOLDER/$NODEJS_VHOST.crt -noout -text
}

function menu_certificates
{
  response=""
  while ! echo $response | grep -i "[b]" > /dev/null
  do
    echo ""
    echo "1) Generate new self-signed certificate"
    echo "2) Generate CSR"
    echo "3) Help to use custom certificate"
    echo "4) View current Certificate"
    echo "b) Back"
    echo "Please make a choice"
    read response
    case $response in
      "1") new_certificate;;
      "2") new_csr;;
      "3") help_certificate;;
      "4") read_certificate;;
      "b") menu_main;;
    esac
  done
}

################################################################################
############################    CREATE DOCKER IMAGES
################################################################################
function pull_image # $Xx_IMG
{
    echo ""
    if [ `$DOCKER images | cut -d" " -f1 | grep $1$ | wc -l` -eq 0 ]
    then
	echo -e "${INFOC}INFO${NC}: $1 image is not present. Installing it..."
	$DOCKER pull $1
	if [ $? -eq 0 ]
	then
	    echo -e "${INFOC}INFO${NC}: $1 image is now installed."
	else
	    echo -e "${ERRORC}ERROR${NC}: $1 image can't be installed."
	fi
    else
	echo -e "${INFOC}INFO${NC}: $1 image is already installed."
    fi
}

function check_image #$XX_IMG
{
  echo ""
  if [ `$DOCKER images | grep "$1" | wc -l` -eq 0 ]
  then
    echo -e "${WARNINGC}WARNING${NC}: Docker Image $1 is not installed."
    echo "         Please deploy all the needed images to run the Application"
    echo "         in a Docker environment."
  else
    echo -e "${INFOC}INFO${NC}: Docker Image $1 is installed"
  fi
}


function deploy_images
{
  pull_image $NGINX_IMG
  pull_image $APP_IMG
}

function remove_images
{
    $DOCKER rmi $NGINX_IMG
  $DOCKER rmi $APP_IMG
}

function check_images
{
  check_image $NGINX_IMG
  check_image $APP_IMG
}

function menu_images
{
  response="0"
  while ! echo $response | grep -i "[b]" > /dev/null
  do
    echo ""
    echo "1) Deploy Docker Images"
    echo "2) Remove Application Image"
    echo "3) Remove Application and Dependencies Images"
    echo "4) Check Docker Images"
    echo "b) Back"
    echo "Please make a choice"
    read response
    case $response in
      "1") deploy_images;;
      "2") $DOCKER rmi $APP_IMG;;
      "3") remove_images;;
      "4") check_images;;
    esac
  done
  response=""
}
################################################################################
############################    CREATE DOCKER CONTAINERS
################################################################################

function create_nginx_container
{
    echo ""
    if [ `$DOCKER ps -a | grep $NGINX_NAME | wc -l` -eq 0 ]
    then
	echo -e "${INFOC}INFO${NC}: $NGINX_NAME container not present. Creating it..."
	$DOCKER create \
	    -p 80:80 \
	    -p 443:443 \
	    --security-opt label:disable \
	    -v $NGINX_CERTS_FOLDER:/etc/nginx/certs:ro \
	    -v /etc/nginx/vhost.d \
	    -v /usr/share/nginx/html \
	    -v /var/run/docker.sock:/tmp/docker.sock:ro \
	    --name=$NGINX_NAME \
	    --restart="on-failure:5" \
	    $NGINX_IMG
	if [ $? -eq 0 ]
	then
	    echo -e "${INFOC}INFO${NC}: $NGINX_NAME container is now created."
	else
	    echo -e "${ERRORC}ERROR${NC}: $NGINX_NAME container can't be created."
	fi
    else
	echo -e "${INFOC}INFO${NC}: $NGINX_NAME container is already created."
    fi
}

function check_container # $XX_NAME
{
  if [ `$DOCKER ps | grep -c "$1"` -gt 0 ]
  then
    echo "$1: INSTALLED and RUNNING"
  elif [ `$DOCKER ps -a | grep -c "$1"` -gt 0 ]
  then
    echo "$1: INSTALLED and STOPPED"
  else
    echo "$1: NOT INSTALLED"
  fi
}
function start_container # $XX_NAME
{
  echo ""
  if [ ! -f $PERSISTANT_FOLDER/$APP_NAME/config.py ]
  then 
    echo -e "${WARNINGC}WARNING${NC}:The script is creating the file $PERSISTANT_FOLDER/$APP_NAME/config.py"
    echo -e "         but you'll have to configure it before starting the app."
    touch $PERSISTANT_FOLDER/$APP_NAME/config.py
    cat <<\EOF > $PERSISTANT_FOLDER/$APP_NAME/config.py

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
# site_id_ignored:      Array of site ids you want to ignore (mwtt will 
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
EOF
    return 1
  else 
    if [ `$DOCKER ps -a | grep $1 | wc -l` -eq 0 ]
    then
      echo -e "${ERRORC}ERROR${NC}: $1 container is not created. Please create it before."
      retval=1
    elif [ `$DOCKER ps | grep $1 | wc -l` -eq 0 ]
    then
      echo -e "${INFOC}INFO${NC}: $1 container is not started. starting it..."
      CID=`$DOCKER ps -a | grep $1 | cut -d" " -f1`
      $DOCKER start $CID
      retval=$?
      if [ $retval -eq 0 ]
      then
        echo -e "${INFOC}INFO${NC}: $1 container is now started."
        retval=0
      else
        echo -e "${ERRORC}ERROR${NC}: $1 container can't be started."
        retval=1
      fi
    else
      echo -e "${INFOC}INFO${NC}: $1 container is alreay running."
      retval=0
    fi
    return $retval
  fi
}

function result_banner
{
  echo ""
  echo ""
  echo "============================================================================"
  echo "============================================================================"
  echo "                  The system is now up and running!"
  echo ""
  echo -e "${INFOC}INFO${NC}: NGINX SSL/TLS certifcates are in $NGINX_CERTS_FOLDER"
  echo ""
  echo -e "${INFOC}INFO${NC}: $APP_NAME interface should now be avaible soon"
  echo "      https://$NODEJS_VHOST"
  echo ""
  echo "============================================================================"
  echo "============================================================================"
}

function start_containers
{

  start_container $NGINX_NAME
  retvalNGINX=$?
  start_container $APP_NAME
  retvalAPP=$?
  if  [ $retvalNGINX -eq 0 ] && [ $retvalAPP -eq 0 ]
  then
    result_banner
  else
    echo ""
    echo -e "${WARNINGC}WARNING${NC}: Some containers are not started. The Application may not"
    echo "         be accesssible."
    echo "         Please fix the errors and retry."
  fi
  echo ""
}


function create_containers
{
  create_nginx_container
  create_app_container $APP_NAME $VHOST
}

function remove_force_container
{
  $DOCKER rm -f $1 > /dev/null
  if [ $? -eq 0 ]
  then
    echo -e "${INFOC}INFO${NC}: $APP_NAME container is now removed."
  else
    echo -e "${ERRORC}ERROR${NC}: $APP_NAME container can't be removed."
  fi
}

function remove_container
{
  if [ `$DOCKER ps | grep $1 | wc -l` -gt 0 ]
  then
    echo -e "${INFOC}INFO${NC}: Container $1 is still running. Are you sure you want to remove it?"
    response=""
    while ! echo "$response" | grep -i "[yn]" > /dev/null
    do
      read -p "Force the removal (y/n)? " response
      case $response in
        "Y"|"y") remove_force_container $1;;
      esac
    done
  elif [ `$DOCKER ps -a | grep $1 | wc -l` -gt 0 ]
  then
    $DOCKER rm $1 > /dev/null
    if [ $? -eq 0 ]
    then
      echo -e "${INFOC}INFO${NC}: $1 container is now removed."
    else
      echo -e "${ERRORC}ERROR${NC}: $1 container can't be removed."

    fi
  else
    echo -e "${INFOC}INFO${NC}: Container $1 is not present. No need to remove it..."
  fi
}

function remove_containers
{
  remove_container $NGINX_NAME
  remove_container $APP_NAME
}

function stop_container # $XX_NAME
{
  if [ `$DOCKER ps | grep $1 | wc -l` -gt 0 ]
  then
    echo -e "${INFOC}INFO${NC}: $1 container is running. stopping it..."
    echo ""
    $DOCKER stop $1
    retval=$?
    if [ $retval -eq 0 ]
    then
      echo -e "${INFOC}INFO${NC}: $1 container is now stopped."
      retval=0
    else
      echo ""
      echo -e "${ERRORC}ERROR${NC}: $1 container can't be stopped."
      retval=1
    fi
  else
    echo -e "${INFOC}INFO${NC}: $1 container was not started."
    retval=0
  fi
  return $retval
}
function stop_containers
{
  stop_container $NGINX_NAME
  stop_container $APP_NAME
}
function check_containers
{
  check_container $NGINX_NAME
  check_container $APP_NAME
}
function menu_containers
{
  response="0"
  while ! echo $response | grep -i "[b]" > /dev/null
  do
    echo ""
    echo "1) Create Docker Containers"
    echo "2) Remove Application Container"
    echo "3) Remove Application and Dependencies Containers"
    echo "4) Check Docker Containers"
    echo "5) Start Docker Containers"
    echo "6) Stop Application Containers"
    echo "7) Stop Application and Dependencies Containers"
    echo "8) Restart Application Container"
    echo "9) Restart Application and Dependencies Containers"
    echo "b) Back"
    echo "Please make a choice"
    read response
    case $response in
      "1") create_containers;;
      "2") remove_container $APP_NAME;;
      "3") remove_containers;;
      "4") check_containers;;
      "5") start_containers;;
      "6") stop_container $APP_NAME;;
      "7") stop_containers;;
      "8") stop_container $APP_NAME; start_container $APP_NAME;;
      "9") stop_containers; start_containers;;
    esac
  done
}


################################################################################
############################    DEPLOY
################################################################################
function auto_deploy
{
  deploy_images
  create_containers
  start_containers
}

function deploy
{
  echo "-----=============-----"
  echo "--=== DEPLOY INIT ===--"
  echo ""
  echo ""
  echo "This script will automatically"
  echo "  - Download Docker Images (NGINX, App)"
  echo "  - Create Docker Containers based on the configuration you gave"
  echo "  - Start Docker Containers"
  echo ""
  response=""
  while ! echo "$response" | grep -i "[yn]" > /dev/null
  do

    read -p "Do you want to continue (y/n)? " response
    case $response in
      "y"|"Y") auto_deploy;;
    esac
  done
}

################################################################################
############################    UPDATE
################################################################################
function update_app
{
  stop_container $APP_NAME
  remove_container $APP_NAME
  $DOCKER rmi $APP_IMG
  pull_image $APP_IMG
  create_app_container
  start_container $APP_NAME
}


################################################################################
############################    INIT
################################################################################
function check_docker
{
  DOCKER=`which docker`
  if ! echo "$DOCKER" | grep -i "docker" > /dev/null
  then
    echo -e "${ERRORC}ERROR${NC}: Unable to find docker path."
    echo "       Plese install docker first: https://www.docker.com/products/overview"
    echo "Exiting..."
    exit 255
  else
    echo -e "${INFOC}INFO${NC}: docker found at $DOCKER"
  fi
}

function init_script
{
  banner "$APP_NAME Management Script"

  check_docker

  init_script_conf

  check_folder "Certificates" $NGINX_CERTS_FOLDER
  check_folder "App" "$PERSISTANT_FOLDER/$APP_NAME"
  check_folder "bower_components" "$PERSISTANT_FOLDER/bower_components"

  check_certificates

  echo -e "${INFOC}INFO${NC}: Script init done."
  echo "||============================================================================="
}

function menu_app
{
  response="0"
  while ! echo $response | grep -i "[b]" > /dev/null
  do
    echo ""
    echo "1) Manage Docker Images"
    echo "2) Manage Docker Containers"
    echo "3) View Application Status"
    echo "b) Back"
    echo "Please make a choice"
    read response
    case $response in
      "1") menu_images;;
      "2") menu_containers;;
      "3") check_containers;;
    esac
  done
}

function menu_main
{
  response="0"
  while ! echo $response | grep -i "[x]" > /dev/null
  do
    echo ""
    echo "1) Deploy and Start Application"
    echo "2) Start Application Containers"
    echo "3) Update Application"
    echo "4) Manage Application"
    echo "5) HTTPS certificates"
    echo "6) Script parameters"
    echo "x) Exit"
    echo "Please make a choice"
    read response
    case $response in
      "1") deploy;;
      "2") start_containers;;
      "3") update_app;;
      "4") menu_app;;
      "5") menu_certificates;;
      "6") menu_script;;      
      "x") exit 0;;
    esac
  done
}


################################################################################
############################    USAGE
################################################################################
usage ()
{
cat <<EOF

NAME
        $SCRIPT_NAME - Installation, Configuration and Control script
                    for $APP_NAME app

SYNOPSIS
        $SCRIPT_NAME [WORD]

DESCRIPTION
        This script will run the action to install, configure and control the
        needed docker containers for Get-a-Key web app.

options are
        start         Validates the configuration and starts all the containers
                      If needed, this will download and install all the needed
                      containers.
        stop          Stops all the containers.
        restart       Same as "stop all" and "start all"
        list          List the containers used by this app.

        help          this help
EOF
}




################################################################################
############################    ENTRY POINT
################################################################################


if [ $# -eq 0 ]
then
  init_script
  menu_main
elif [ $# -eq 1 ]
then
  case $1 in
    "start") init_script; start_containers;;
    "stop") init_script; stop_containers;;
    "restart") init_script; stop_containers; start_containers;;
    "list") init_script; check_containers;;
    *) usage; exit 1;;
  esac
else
  usage
  exit 1
fi