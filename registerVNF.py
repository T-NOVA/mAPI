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
    print "\nCreating VNF Folder:"
    folder = mapi_folder + 'VNF_Library/VNF_' + str(vnf_id) + '/'
    if not path.exists(folder):
      makedirs(folder)
    print "ok"
    if vnf_descriptor['lifecycle_event']['Authentication_Type'] == 'private key':
      print "\nAuthentication with private key, saving key:"
      with open(mapi_folder + "keys/" + vnf_id + ".pem", 'w') as pemFile:
        pemFile.write(vnf_descriptor['lifecycle_event']['Authentication'])
        print "ok"
    #create resources in Rundeck and store data in DB
    print "\nCreating project in Rundeck:"
    vnf_url = create_project(vnf_id, vnf_descriptor['lifecycle_event'])
    print "ok"
    print "\nSaving VNF data in DB:"
    print vnf_id, vnf_url,vnf_descriptor['lifecycle_event']['Authentication_Username']
    vnf_obj = db.add_VNF(vnf_id, vnf_url,vnf_descriptor['lifecycle_event']['Authentication_Username'])
    print "ok"
    for event in vnf_descriptor["lifecycle_event"]['events']:
      event["VNF Folder"] = folder
      event["VNF Container"] = vnf_descriptor["lifecycle_event"]["VNF_Container"]
      print "\nCreating Job in Rundeck:"
      job_url = create_job(vnf_id, event)
      print "ok"
      #write templates to files
      print "\nSaving template files:"
      if event.has_key("Template File Format"):
        if event["Template File Format"] == 'xml':
          fromstring(job["Template File"]).write(mapi_folder + "VNF_Library/VNF_" + vnf_id + '/' + event["Event"] + '.xml', encoding="UTF-8", xml_declaration=True)
        elif event["Template File Format"] == 'json':
          with open(mapi_folder + "VNF_Library/VNF_" + vnf_id + '/' + event["Event"] + '.json', 'w') as jsonfile:
            jsonfile.write(event["Template File"])
      print "ok"
      print "\nSaving Event data in DB:"
      db.add_event(event["Event"], job_url, vnf_obj)
      print "ok"
