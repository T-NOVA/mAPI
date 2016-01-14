# T-NOVA platform - Middleware API

## Description

The Middleware API component enables lifecycle management of Virtual Network Functions (VNF). According to ETSI's NFV-MANO specification this component realizes the Ve-Vnfm reference point.

### Version

- 0.61

### Changes

#### 0.1
- VNF Registering Interface created

#### 0.5
- Lifecycle management interface created
- mAPI now provides better feedback during execution
- Keys folder added to store VDUs private key authentication (pem file)
- test folder contains examples of VNFDs and configuration requests 

#### 0.6
- Updated VNF register: username and private key are now uploaded in the VNFD

#### 0.61
- Added support for the new version of the VNF descriptor
- Corrected the README.MD
- Correct a bug when storing the pem key

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
- Rundeck - 2.4.2, 2.5.3
- MySQL - 5.5.43

## Install Guide

This guide was tested in Ubuntu 14.04 LTS

### Install Rundeck

1. Go to page http://rundeck.org
2. Scroll to section "Debian/Ubuntu Install" and copy the download link 
3. In terminal do: 

```
  wget "download link" (in our case it was http://dl.bintray.com/rundeck/rundeck-deb/rundeck-"version"-GA.deb)
```

```
  sudo apt-get install openjdk-7-jdk
```

```
  sudo dpkg -i rundeck-"version"-GA.deb 
```

#### Rundeck project creation permissions

It is necessary to give authorization to create projects using the API

The file apitoken.aclpolicy in /etc/rundeck/ should look like this

```
description: API project level access control
context:
  project: '.*' # all projects
for:
  resource:
    - equals:
        kind: job
      allow: [create,delete,read] # allow create and delete jobs
    - equals:
        kind: node
      allow: [read,create,update,refresh] # allow refresh node sources
    - equals:
        kind: event
      allow: [read,create] # allow read/create events
    - equals:
        kind: project
      allow: [read,create]
  adhoc:
    - allow: [read,run,kill] # allow running/killing adhoc jobs and read output
  job:
    - allow: [create,read,update,delete,run,kill] # allow create/read/write/delete/run/kill of all jobs
  node:
    - allow: [read,run] # allow read/run for all nodes
  project:
    - allow: [create,read,update,delete,import,export,admin]
by:
  group: api_token_group

---

description: API Application level access control
context:
  application: 'rundeck'
for:
  resource:
    - equals:
        kind: system
      allow: [read] # allow read of system info
  project:
    - match:
        name: '.*'
      allow: [admin,import,export,read,create] # allow view of all projects
  storage:
    - match:
        path: '(keys|keys/.*)'
      allow: '*' # allow all access to manage stored keys
by:
  group: api_token_group
```

The file admin.aclpolicy in /etc/rundeck/ should look like this:

```
description: Admin, all access.
context:
  project: '.*' # all projects
for:
  resource:
    - allow: '*' # allow read/create all kinds
  adhoc:
    - allow: '*' # allow read/running/killing adhoc jobs
  job:
    - allow: '*' # allow read/write/delete/run/kill of all jobs
  node:
    - allow: '*' # allow read/run for all nodes
by:
  group: [admin,api_token_group]

---

description: Admin, all access.
context:
  application: 'rundeck'
for:
  resource:
    - allow: '*' # allow create of projects
  project:
    - allow: '*' # allow view/admin of all projects
  storage:
    - allow: '*' # allow read/create/update/delete for all /keys/* storage content
by:
  group: [admin,api_token_group]
```


### Install MySQL

1. sudo apt-get install mysql-server
2. enter admin password, it will be used later to configure the mAPI
3. create mapi database, in terminal do:

```
  mysql -u "username" -p"password"
```

```
  create database mapi;
```

### Install Python dependencies

1. Install Bottle framework

```
sudo apt-get install python-bottle
```

2. Install SQLAlchemy

```
sudo apt-get install python-sqlalchemy
```

```
sudo apt-get install python-mysqldb
```

### Get mAPI code
 

## Configuration

To configure the Middleware API you can use the mAPI.cfg file present in the 'Config' folder.

### Configuration Parameters

#### authentication

authentication_method - two mechanisms are available, basic authentication and gatekeeper). Gatekeeper is the official authentication mechanism used in T-NOVA, while basic is only username:password authentication. 

username - username for mAPI northbound interface authentication (basic authentication)

password - password for mAPI northbound interface authentication (basic authentication)

gatekeeper_host - Gatekeeper IP Address or DNS name location 

gatekeeper_port - Port where Gatekeeper is listening

service_key - Token assigned to mAPI by Gatekeeper

#### server

ip - IP address for the mAPI northbound interface

port - Port number for the mAPI norhbound interface

#### general

folder - folder location of the mAPI software

#### rundeck

host - IP address or DNS name of the host where Rundeck is running

port - Port number used by the Rundeck API

token - authentication token used in Rundeck

project folder - folder location of Rundeck projects folder

TNOVA_user - username associated with the private key, it will be used with the SSH driver to access the VDUs

#### db

user - username for MySQL database authentication

password -  password for MySQL database authentication

ip - IP address of MySQL server

### Example configuration

Because this is just an example some sections remained unchanged:
1. Authentication
2. Server (using 0.0.0.0 allows the mAPI to listen on all interfaces)

#### "general" Section

1. Set the mAPI folder variable

#### "rundeck" Section

1. We will need to start Rundeck to retrieve the authentication token. Rundeck default configuration sets the GUI to localhost, if you want outside access to the GUI it is needed to change the configuration. 
  1. Change the variable "grails.serverURL" in /etc/rundeck/rundeck-config.properties to the IP address of your choice (skip this step if don't want outside access to the GUI)
  2. If you're running the mAPI in VM in OpenStack don't forget to change the Security Groups to allow TCP on port 4440
  3. Enter the Rundeck URL in your browser ("IP address":4440)
  4. Username and password for the admin user are admin:admin
  5. Go to admin>Profile and enter a mail address
  6. Next click on "generate new token"
  7. Copy the token to the mAPI.cfg file to where it says token

#### "db" Section 

1. Set the password and user for MySQL

## Running Middleware API

The Middleware API needs to run with sudo because some operations are normally limited to superusers.
To run the Middleware API just type in terminal:

 ~/mAPI_folder/sudo python northboundinterface.py

### VNF registration example

Bellow you can find an example of the information that the VNFM sends to the mAPI to register a new VNF. The json file is comprised of the following elements:
* id - the VNFR Id which identifies the specific VNF instance
* vnfd - the VNF Descriptor (note: here is shown a partial VNFD with only the lifecycle management related sections):

```json
{
  "id":"localvNF",
  "vnfd": {
    "vnf_lifecycle_events":{
      "driver":"SSH",
      "authentication":"-----BEGIN RSA PRIVATE KEY-----MIIEpAIBAAKCAQEA0QtIBRduKsYTmabyMHi5FoqZOrEmMSnoTLtkRBYTmkICqsYaHyiHyvAzFKBbg81ze9KlUo8GhDM71BRxpkswsvmLHRHwTGfauPWUNszb0ZaIK+zqOolVUDTa8x5wXZ1/SsJeUzYZrYdH8YNUhpLIk4XLZoyJbxfJ+40lRjtARV+VJGlEgGU74cCoj1gy9OafhvfCsGxaA4GygQa3LkWGYt1KR8Y1lCa7yaq3apJBCRxvpQ3Mdr8v9WaCaJ3suqoRaisvxwIWs71VI8UkNhQ6ts6ki2mQKSr2V7/mIWfpu9Yde93EFt/r417FBpmCqT/UkLlvahvtjTotXcnL84/mEwIDAQABAoIBAQDKhjh3HlUQQaiZkyFOjpca3JpJP3k15lj1hhNE13KUX2GAG78Q8s5kcUO7twQSdIhurQyYKJLyn0RWWpwktPHwY01Ak7GQBInl6Z53XQ+WRVWV4Miof4bU1vBM2++W8tBxGFAUI/TKpqavuEG6wxhpvBTsPDmmFJEOEZfMK/k/evI7D4TcoHfz6pZYoea3Qv7THoJ4mOwDwRmJMztm/hSrHKSz3lJ9xlyAkfnmFanwlF1IzNHfbHOyGrRaMrRlGUVhDJUP9R1l57n3rHv8wgPizGLU7ot1H0WRkYqd58Imq76sOQ1PEQU0vbW+jCdQt+FSAqu5dWK+nG5R07Oqc1ahAoGBAPpOGlZZYl3yPj0KGJRSFcaWflHzTrVTS28zSNfydsSL3wSWmnHup+HJg0gteOlW1abiomDMls5PkuHES8lBOBWMZlnwOD6oVDR2jVi6Ck1zsCA51ykfHwL40jItCktoER4+IEW9M/B8jugKCmoOhHoVXPMLMs/X5gorwTepTtfjAoGBANXM2rvuERfjnwFiABMrpyksrIbXZf+AQ3+j9SXBYT40SX0kK3wOEIIh/whX4otbTmrPf7HJhmGxo34LUADXP+vdws+SOob0QCz9Ep8qGgccmNG38PtwsFqysAeWWO7hL6w4OLpI23cQ877b3k/sVFhjxkLFGYXQIuZS/potEzARAoGAapqpDO20v15Us5qBLWpoa9PcqPp/Iyr+jbXB6HcTrlIEAehCjxOd3MP+bdcwD/EzvYf4sFFySRwK6qy3uldUk5jgXp241rbKZi23tXpGuQX0lUUNJi5i/tkKbORR5hvEbqT3CbyzSlFCbAEavmDAe15t3/V9BphlGR/ZguNQ+RECgYB2+OD7VPX0GjkgNt2dzVve4Lo86t4aeNCW1bEUSnEHgWcnmRoNlXIASFS32tf4/l07uK3xTBhYgtZczIS/gwhSA3xlr5ScBo0zu7xCD9aeAH7VrQsPkFzCi87C2hoxC+RQbJS8rNBbiHZqzcT/Kp6g9RydiTqzqOfSzXpaZxzXUQKBgQC+q/lIN8YfNbx+sC0cH5GdK7fTmEVUvx93rJM8iCknWU6mL56e0ddeZD8f2SHJhHyoEsH7v0JFHYasXDb7s7b4JNm10RLD/IbOaOBiNv4yynS9boLjvHqIWlbpNaMdd0SBjNghNOdHerF338Dd9Hdwl3o5QHnp/4kjZHPI2Jc+rw==-----END RSA PRIVATE KEY-----",
      "authentication_type":"private key",
      "authentication_username":"ubuntu",
      "vnf_container":"/home/bsendas/container/",
      "events":[
        "start":{
          "Command":"python /home/bsendas/local_vnf/start.py",
          "Template File Format":"json",
          "Template File":"{ \"controller\":\"get_attr[vdu1,PublicIp]\", \"vdu1\":\"get_attr[vdu1,PublicIp]\", \"vdu2\":\"get_attr[vdu2,PrimaryPrivateIpAddress]\" }"
        },
        "stop":{
          "Command":"python /home/bsendas/local_vnf/stop.py"
        },
        "halt":{
          "Command":"python /home/bsendas/local_vnf/halt.py",
          "Template File Format":"json",
          "Template File":"{\"controller\":\"get_attr[vdu1,PublicIp]\",\"vdu1\":\"get_attr[vdu1,PublicIp]\",\"vdu2\":\"get_attr[vdu2,PrimaryPrivateIpAddress]\"}"
        }
      ]
    }
  }
}
```

To upload this VNFD to mAPI you can use cURL:

curl -X POST 0.0.0.0:1234/vnf_api/ -u admin:changeme -d @~/mAPI/test/temp_local.json -v

### VNF start event example

Here is shown an example for the VNF initial/start configuration triggerbasing on the registering example shown above. The request file sent by the the VNFM is comprised of the following elements:
* event - the event this request belongs to
* vnf_controller - the IP address that the mAPI can use to reach the VNFC that manages and configures the VNF
* parameters - the list of instantion specific parameters

```json
{
  "event":"start",
  "vnf_controller":["10.0.2.15"],
  "parameters":{
    "vdu1_PublicIp":["10.0.2.15"],
    "vdu2_PrimaryPrivateIpAddress":["10.0.2.20"]
  }
}
```

To trigger the Start command you can use cURL:

curl -X POST 0.0.0.0:1234/vnf_api/localvNF/config/ -u admin:changeme -d @~/mAPI/test/temp_start.json
