from os import makedirs, path, fork
from Database.mapidb import mapiDB
from Rundeck_Aux.rundeckconnector import create_project, create_job
from xml.etree.cElementTree import fromstring
from Config.configuration import Configuration

conf = Configuration()
mapi_folder = conf.get_mAPI_folder()

def register_vnf(vnf_id, vnf_descriptor):
  child =0
  if child == 0:
    #create DB object
    db = mapiDB()

    #create VNF folder
    folder = mapi_folder + 'VNF_Library/VNF_' + str(vnf_id) + '/'
    if not path.exists(folder):
      makedirs(folder)

    #create resources in Rundeck and store data in DB
    vnf_url = create_project(vnf_id, vnf_descriptor['lifecycle_event'])
    vnf_obj = db.add_VNF(vnf_id, vnf_url)
    for event in vnf_descriptor["lifecycle_event"]['events']:
      event["VNF Folder"] = folder
      event["VNF Container"] = vnf_descriptor["lifecycle_event"]["VNF_Container"]
      job_url = create_job(vnf_id, event)
      #write templates to files
      if event.has_key("Template File Format"):
        if event["Template File Format"] == 'xml':
          fromstring(job["Template File"]).write(mapi_folder + "VNF_Library/VNF_" + vnf_id + '/' + event["Event"] + '.xml', encoding="UTF-8", xml_declaration=True)
        elif event["Template File Format"] == 'json':
          with open(mapi_folder + "VNF_Library/VNF_" + vnf_id + '/' + event["Event"] + '.json', 'w') as jsonfile:
            jsonfile.write(event["Template File"])
      db.add_event(event["Event"], job_url, vnf_obj)
