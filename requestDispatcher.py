import xml.etree.cElementTree as ET
#from Database.mapidb import mapiDB
import Database.mapidb2 as db
from Rundeck_Aux.rich_template import enrich_config_template
from Rundeck_Aux.rundeckconnector import add_node, execute_job, delete_project, is_job_running, list_jobs, update_job 
from Config.configuration import Configuration
import shutil
import json

conf = Configuration()
##TNOVA_user = conf.get_TNOVA_user()
mapi_folder = conf.get_mAPI_folder()
#db = mapiDB()

def get_current_configuration(vnf_id):
  try:
    with open(mapi_folder + "VNF_Library/VNF_" + vnf_id + "/current.json", "r") as current_config:
      conf_obj = json.loads(current_config.read())
    return conf_obj
  except:
    return False

def initial_configuration(vnf_id, vnfm_request_file):
  try:
    # access DB and retrieve event info
    print  "\nVNF ID: " + vnf_id 
    event = db.get_event('start', db.get_VNF(vnf_id))
    print "\nEvent: " + str(event) + "\n"
    if vnfm_request_file:
      if vnfm_request_file.has_key('parameters') and not vnfm_request_file['parameters'] == {}:
      # build configuration file if applicable
        with open(mapi_folder + "VNF_Library/VNF_" + vnf_id + "/" + "start" + ".json", "r") as template:
          json_obj = enrich_config_template(vnfm_request_file['parameters'], json.loads(template.read()))
          print '\nConfiguration file ready:\n'
          print json_obj
          with open(mapi_folder + "VNF_Library/VNF_" + vnf_id + "/current.json", "w") as json_file:
            json_file.write(json.dumps(json_obj))
    else:
      vnfm_request_file = {}
    print "\nVNF Controller info: \n"
    print "VNF Controller : " + vnfm_request_file['vnf_controller'] + '\n'
    print "VM username: " + event.vnf.username + '\n'
    # add node to rundeck
    add_node(vnf_id, vnfm_request_file['vnf_controller'], event.vnf.username)
    # update jobs with the VNFC ip only when the HTTP driver is used
    jobs = list_jobs(vnf_id)
    root = ET.fromstring(jobs)
    for job in root.findall('job'):
      update_job(job.attrib['id'], vnfm_request_file['vnf_controller'], vnf_id)

    # trigger job execution
    execute_job(event.jobUrl)
    print "End of VNF initial configuration\n"
    return True
  except:
    return False

def update_configuration(vnf_id, vnfm_request_file):
  try:
    event = db.get_event(vnfm_request_file["event"], db.get_VNF(vnf_id))
    if vnfm_request_file.has_key('parameters') and not vnfm_request_file['parameters'] == {}:
      print "the new configuration has a request file"
      with open(mapi_folder + "VNF_Library/VNF_" + vnf_id + "/" + vnfm_request_file["event"] + ".json", "r") as template:
        json_obj = enrich_config_template(vnfm_request_file['parameters'], json.loads(template.read()))
        print '\nConfiguration file ready:\n'
        print json_obj
        with open(mapi_folder + "VNF_Library/VNF_" + vnf_id + "/current.json", "w") as json_file:
          json_file.write(json.dumps(json_obj))
    print "Trigger job execution "
    print event.jobUrl
    execute_job(event.jobUrl)
    print "End of VNF configuration workflow\n"
    return True
  except:
    return False

def delete_vnf(vnf_id, vnfm_request_file = None):
  try:
    if vnfm_request_file:
      if vnfm_request_file.has_key('parameters') and not vnfm_request_file['parameters'] == {}:
        print "the stop operation has request file"
        with open(mapi_folder + "VNF_Library/VNF_" + vnf_id + "/" + vnfm_request_file["event"] + ".json", "r") as template:
          json_obj = enrich_config_template(vnfm_request_file['parameters'], json.loads(template.read()))
          with open(mapi_folder + "VNF_Library/VNF_" + vnf_id + "/current.json", "w") as json_file:
            json_file.write(json.dumps(json_obj))
    event = db.get_event('stop', db.get_VNF(vnf_id))
    response = execute_job(event.jobUrl)
    response = ET.fromstring(response)
    while is_job_running(response.find("./execution/job").attrib['id']):
      print '\nwaiting for job to finish'
    vnf = db.get_VNF(vnf_id)
    # remove project from rundeck
    print "\nStarting Rundeck project removal:"
    status = delete_project(vnf.projectUrl)
    if status == '500':
      for i in range(5):
        status = delete_project(vnf.projectUrl)
        if status == '204':
          continue
      print '\nError: failed to remove project from Rundeck'
    print "Ok"
    print "\nDeleting VNF files in " + mapi_folder + "VNF_Library/VNF_" + vnf_id + "/ :"
    # remove files from VNF folder
    shutil.rmtree(mapi_folder + "VNF_Library/VNF_" + vnf_id + "/")
    print "Ok"
    # remove DB data
    print "\nDelete VNF registry:"
    db.delete_VNF(vnf)
    print "Ok"
    print "\nEnd of VNF removal workflow\n"
    return True
  except:
    return False
