# T-NOVA platform - Middleware API

## Description

The Middleware API component enables lifecycle management of Virtual Network Functions (VNF). According to ETSI's NFV-MANO specification this component realizes the Ve-Vnfm reference point.

### Version

- 0.1

### Changes

- VNF Registering Interface created

## Requirements

- Bottle: Python Web Framework (URL: http://www.bottlepy.org)
- SQLAlchemy: The Database Toolkit for Python (URL: http://www.sqlalchemy.org)
- Rundeck: Job Scheduler and Runbook Automation (URL: http://www.rundeck.org)
- MySQL: Open-Source Database (URL: https://www.mysql.com)

## Tested Configuration

### Software Versions
- Ubuntu - 14.04
- Python - 2.7.6
- Bottle - 0.12
- SQLAlchemy - 0.8.4
- Rundeck - 2.4.2
- MySQL - 5.5.43

## Configuration

To configure the Middleware API you can use the mAPI.cfg file present in the 'Config' folder.

### Configuration Parameters

#### authentication

username - username for mAPI northbound interface authentication

password - password for mAPI northbound interface authentication

#### server

ip - IP address for the mAPI northbound interface

port - Port number for the mAPI norhbound interface

#### general

folder - folder location of the mAPI software

#### rundeck

host - IP address of the host where Rundeck is running

token - authentication token used in Rundeck

project folder - folder location of Rundeck projects folder

#### db

user - username for MySQL database authentication

password -  password for MySQL database authentication

ip - IP address of MySQL server


## Running Middleware API

To run the Middleware API just type in terminal:

 ~/mAPI_folder/python run.py

### VNF registration example

Bellow you can find an example of a partial VNF Descriptor (with only the lifecycle management related sections):

{

  "id":"vTC3", 

  "lifecycle_event":{

    "Driver":"SSH",

    "Authentication":"private_key.pem",

    "Authentication_Type":"private key",

    "VNF_Container":"/home/vtc/container/",

    "events":[

      {

        "Event":"start", 

        "Command":"service vtc start", 

        "Template File Format":"json", 

        "Template File":"{ \"controller\":\"cntr_IP\", \"vdu1\":\"vdu1_IP\", \"vdu2\":\"vdu2_IP\" }"

      },

      {

        "Event":"stop",

        "Command":"service vtc stop",

        "Template File Format":"json",

        "Template File":"{\"controller\":\"cntr_IP\",\"vdu1\":\"vdu1_IP\",\"vdu2\":\"vdu2_IP\"}"

      },

      {

        "Event":"halt",

        "Command":"service vtc shutoff",

        "Template File Format":"json",

        "Template File":"{\"controller\":\"cntr_IP\",\"vdu1\":\"vdu1_IP\",\"vdu2\":\"vdu2_IP\"}"

      }

    ]

  }

}

To upload this VNFD to mAPI you can use cURL:

curl -X POST 0.0.0.0:1234/vnf_api/ -u admin:changeme -d @~/mAPI/temp.json -v
