from os import makedirs, path, fork
from Database.mapidb import mapiDB
from Rundeck_Aux.rundeckconnector import create_project, create_job
from xml.etree.cElementTree import fromstring
from Config.configuration import Configuration
from Auxiliary.key_fixer import keyFixer

conf = Configuration()
mapi_folder = conf.get_mAPI_folder()

def register_vnf(vnf_id, vnf_descriptor):
  child =0
  if child == 0:
    #create DB object
    db = mapiDB()

    #create VNF folder
    print "\nCreating VNF Folder:"
    folder = mapi_folder + 'VNF_Library/VNF_' + str(vnf_id) + '/'
    if not path.exists(folder):
      makedirs(folder)
    print "ok"
    if vnf_descriptor['vnf_lifecycle_events']['authentication_type'] == 'PubKeyAuthentication':
      print "\nAuthentication with private key, saving key:"
      keyFixer(mapi_folder, vnf_id, vnf_descriptor['vnf_lifecycle_events']['authentication']).parseKey()
#      with open(mapi_folder + "keys/" + vnf_id + ".pem", 'w') as pemFile:
 #       pemFile.write(vnf_descriptor['vnf_lifecycle_events']['authentication'])
      print "ok"
    #create resources in Rundeck and store data in DB
    print "\nCreating project in Rundeck:"
    vnf_url = create_project(vnf_id, vnf_descriptor['vnf_lifecycle_events'])
    print "ok"
    print "\nSaving VNF data in DB:"
    print vnf_id, vnf_url,vnf_descriptor['vnf_lifecycle_events']['authentication_username']
    vnf_obj = db.add_VNF(vnf_id, vnf_url,vnf_descriptor['vnf_lifecycle_events']['authentication_username'])
    print "ok"
    for elem in vnf_descriptor["vnf_lifecycle_events"]['events'].items():
      if elem[1] is not None:
        event = elem[1]
        event["Event"] = elem[0]
        event["VNF Folder"] = folder
        event["VNF Container"] = vnf_descriptor["vnf_lifecycle_events"]["vnf_container"]
        event["authentication_type"] = vnf_descriptor["vnf_lifecycle_events"]["authentication_type"]
        if vnf_descriptor['vnf_lifecycle_events']['authentication_type'] == 'HTTPBasicAuth':
          if vnf_descriptor['vnf_lifecycle_events']['authentication_port'] is not None:
            event["authentication_port"] = vnf_descriptor['vnf_lifecycle_events']['authentication_port']
            event["authentication_username"] = vnf_descriptor['vnf_lifecycle_events']['authentication_username']
            event["authentication"] = vnf_descriptor['vnf_lifecycle_events']['authentication']
        print "\nCreating Job in Rundeck:"
        job_url = create_job(vnf_id, event)
        print "ok"
        #write templates to files
        print "\nSaving template files: " + mapi_folder + "VNF_Library/VNF_" + vnf_id + '/' + event["Event"] + '.json'
        if event.has_key("template_file_format"):
          if event["template_file_format"].lower() == 'xml':
            fromstring(job["template_file"]).write(mapi_folder + "VNF_Library/VNF_" + vnf_id + '/' + event["Event"] + '.xml', encoding="UTF-8", xml_declaration=True)
          elif event["template_file_format"].lower() == 'json':
            with open(mapi_folder + "VNF_Library/VNF_" + vnf_id + '/' + event["Event"] + '.json', 'w') as jsonfile:
              jsonfile.write(event["template_file"])
        print "ok"
        print "\nSaving Event data in DB:"
        db.add_event(event["Event"], job_url, vnf_obj)
        print "ok"
      else:
        continue
