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
- Ubuntu
- Python
- Bottle
- SQLAlchemy
- Rundeck
- MySQL

## Configuration

To configure the Middleware API you can use the mAPI.cfg file present in the 'Config' folder.

### Configuration Parameters
| Section        | Parameter      | Value  | Description |
| -------------- | -------------- | ------ | ----------- |
| authentication | username       | string | username for mAPI northbound interface authentication|
| authentication | password       | string | password for mAPI northbound interface authentication|
| server         | ip             | string | IP address for the mAPI northbound interface|
| server         | port           | string | Port number for the mAPI norhbound interface|
| general        | folder         | string | folder location of the mAPI software|
| rundeck        | host           | string | IP address of the host where Rundeck is running|
| rundeck        | token          | string | authentication token used in Rundeck |
| rundeck        | project folder | string | folder location of Rundeck projects folder| 
| db             | user           | string | username for MySQL database authentication|
| db             | password       | string | password for MySQL database authentication| 
| db             | ip             | string | IP address of MySQL server|

## Running Middleware API
