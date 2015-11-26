from Database.mapidb import mapiDB
from Rundeck_Aux.rich_template import enrich_config_template
from Rundeck_Aux.rundeckconnector import add_node, execute_job, delete_project 
from Config.configuration import Configuration
import shutil
import json

conf = Configuration()
TNOVA_user = conf.get_TNOVA_user()
mapi_folder = conf.get_mAPI_folder()
db = mapiDB()

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
    event = db.get_event('start', vnf_id)
    if vnfm_request_file:
      # build configuration file if applicable
      with open(mapi_folder + "VNF_Library/VNF_" + vnf_id + "/" + "start" + ".json", "r") as template:
        json_obj = enrich_config_template(vnfm_request_file['parameters'], json.loads(template.read()))
        print '\nConfiguration file ready:\n'
        print json_obj
        with open(mapi_folder + "VNF_Library/VNF_" + vnf_id + "/current.json", "w") as json_file:
          json_file.write(json.dumps(json_obj))
    print "\nVNF Controller info: \n"
    print "VNF Controller : " + vnfm_request_file['vnf_controller'][0] + '\n'
    print "VM username: " + TNOVA_user + '\n'
    # add node to rundeck
    add_node(vnf_id, vnfm_request_file['vnf_controller'][0], TNOVA_user)
    # trigger job execution
    execute_job(event.jobUrl)
    print "End of VNF initial configuration\n"
    return True
  except:
    return False

def update_configuration(vnf_id, vnfm_request_file):
  try:
    event = db.get_event(vnfm_request_file["event"], vnf_id)
    if vnfm_request_file.has_key('parameters'):
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
      print "the stop operation has request file"
      with open(mapi_folder + "VNF_Library/VNF_" + vnf_id + "/" + vnfm_request_file["event"] + ".json", "r") as template:
        json_obj = enrich_config_template(vnfm_request_file['parameters'], template)
        with open(mapi_folder + "VNF_Library/VNF_" + vnf_id + "/current.json", "w") as json_file:
          jsonfile.write(json_obg)
    event = db.get_event('stop', vnf_id)
    execute_job(event.jobUrl)
    vnf = db.get_VNF(vnf_id)
    # remove project from rundeck
    print "\nStarting Rundeck project removal:"
    delete_project(vnf.projectUrl)
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
