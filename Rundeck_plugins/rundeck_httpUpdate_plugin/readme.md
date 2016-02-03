# T-NOVA platform - RunDeck plugin - HttpUpload

## Description

Add to RunDeck a WorkflowNodeStep plugin that provides  http requests with file uploading. They are http requests (POST, PUT) with basic authentication.

### Version

- 1.5

### Changes

#### 1.5
- First release

## Requirements

- Rundeck: Job Scheduler and Runbook Automation (URL: http://www.rundeck.org)


## Tested Configuration

### Software Versions
- Rundeck - 2.6.1-1
- Java  - 1.7.x
- Apache Ant - 1.9.6

## Install Guide

This guide was tested Windows 7


### Install Rundeck

1. Go to page http://rundeck.org/downloads.html
2. Scroll to section "Self Contained Launcher Install" and press on "rundeck-launcher-2-6-1.jar" to download the jar file.


#### RunDeck

RDECK_BASE - new empty folder where to install Rundeck
  
host - IP address or DNS name of the host where Rundeck is running

port - Port number used by the Rundeck API

token - authentication token used in Rundeck

project folder - folder location of Rundeck projects folder

TNOVA_user - username associated with the private key, it will be used with the SSH driver to access the VDUs



#### Rundeck configuration

Set this environment variables:
RDECK_BASE=<folder where you installed RunDeck>

In RDECK_BASE/server/config
modify the following file (skip this step if don't want outside access to the GUI): 
rundeck-config.properties
adding IP's address of the machine  you are installerd Rundeck in, e.g.:
grails.serverURL=http://111.222.133.244:4440



#### RunDeck execution and plugins list

to run RunDeck:
in RDECK_BASE folder launch following command:
java -jar rundeck-launcher-2.6.1.jar

At first time, rundeck will creare some new subfolders.

To use RunDeck from GUI:
enter the Rundeck URL in your browser ("IP address":4440)
Username and password for the admin user are admin:admin

In all pages, in the right top corner there is a gear-icon (configure). Clicking on it and then on "List plugins" you can see all already installed plugins. 



#### Clone HttpCall RunDeck plugin project from Bitbucket

Clone the project from http://stash.i2cat.net/projects/TNOV/repos/wp5/browse/WP5/mAPI/Rundeck_plugins/rundeck_httpUpdate_plugin


#### Generation of HttpCall RunDeck plugin

Plugins for Rundeck are jar files. To generate HttpCall plugin use the following command:

ant jar -lib lib_nodeploy

a dist folder will be created and inside it the file rundeck-httpupload-plugin-1.5.jar


#### installation in RunDeck of the  HttpCall plugin

copy rundeck-httpupload-plugin-1.5.jar file in RDECK_BASE/libext folder.


#### Verify installation 

Inside RunDeck web interface, see "List plugins". If all previous steps were correct, there should be HTTP File Upload plugin listed in "WorkFlow Node Step" set. 


