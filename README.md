# T-NOVA platform - Middleware API

## Description

The Middleware API component enables lifecycle management of Virtual Network Functions (VNF). According to ETSI's NFV-MANO specification this component realizes the Ve-Vnfm reference point.

### Version

- 0.99

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

#### 0.8
- Integration with T-NOVA VNFM validated
- Created the mAPI.cfg.sample to avoid overwriting the configuration when updating the Middleware API
- Added support for the new version of the VNF descriptor
- Corrected a bug with the VNF validation

#### 0.81
- Updated expected values for some VNFD parameters 

#### 0.82
- Several bugs corrected
- Integrated with VNFM

#### 0.99
- Several bug fixes
- Changed MySQL interface from SQL Alchemy to MySQdb Python library
- Integrated http driver

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
  wget "download link" (in our case it was http://download.rundeck.org/deb/rundeck-2.5.3-1-GA.deb)
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

### VNF examples

In folder ~/mAPI_folder/test you can find some examples of json requests for registering and triggering lifecycle events using mAPI
