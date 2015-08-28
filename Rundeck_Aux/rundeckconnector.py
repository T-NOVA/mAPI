import xml.etree.cElementTree as ET
from Config.configuration import Configuration
import httplib
from json import loads, dumps
from Auxiliary import formdata


conf = Configuration()
mapi_folder = conf.get_mAPI_folder()
rundeck_host = conf.get_rundeck_host()
rundeck_port = conf.get_rundeck_port()
rundeck_token = conf.get_rundeck_token()
rundeck_project_folder = conf.get_rundeck_project_folder()

def post_project(file_as_text):
  print file_as_text
  con = httplib.HTTPConnection(rundeck_host, rundeck_port)
  headers = ({"Content-Type":"application/json",
             "X-Rundeck-Auth-Token":"%s" % rundeck_token})
  con.request('POST', '/api/12/projects', file_as_text, headers = headers)
  response = con.getresponse().read()
  print response
  return loads(response)['url']

def post_job(filename):
  files = {'xmlBatch': {'filename': filename, 'content': open(filename,'rb').read()}}
  data, headers = formdata.encode_multipart({}, files)
  con = httplib.HTTPConnection(rundeck_host, rundeck_port)
  headers["X-Rundeck-Auth-Token"] = "%s" % rundeck_token
  con.request('POST', '/api/12/jobs/import/', data, headers = headers)
  response = con.getresponse()
  xml = ET.fromstring(response.read())
  return xml.find('./succeeded/job').attrib['href']

def delete_project(project_url):
  con = httplib.HTTPConnection(rundeck_host, rundeck_port)
  headers = ({"X-Rundeck-Auth-Token" : "%s" % rundeck_token})
  con.request('DELETE', project_url, headers = headers)

def delete_job(job_url):
  con = httplib.HTTPConnection(rundeck_host, rundeck_port)
  headers = ({"X-Rundeck-Auth-Token" : "%s" % rundeck_token})
  con.request('DELETE', job_url, headers = headers)

def create_project(vnf_id, ems):
  with open(mapi_folder + 'Rundeck_Aux/project_request.json', 'r') as f:
    project_request = loads(f.read())
  project_request['name'] = vnf_id
  if ems['Driver'] == 'SSH':
    if ems['Authentication_Type'] == 'private key':
      project_request['config']['project.ssh-keypath'] = mapi_folder + 'keys/' + ems['Authentication']
  response = post_project(dumps(project_request))
  return response

def add_node(vnf_id, ip_address, vnf_username):
  project = ET.Element("project")
  ET.SubElement(project, "node", name="vnf-mgmt", description="vnf management element", tags="vnf-mgmt", hostname=ip_address,osFamily="unix", username=vnf_username)
  ET.ElementTree(project).write(rundeck_project_folder + vnf_id + "/etc/resources.xml", encoding="UTF-8", xml_declaration=True)

def create_job(vnf_id, job):
  print job
  tree = ET.parse(mapi_folder + 'Rundeck_Aux/job_template.xml')
  root = tree.getroot()
  if "Template File" in job:
    for entry in root.findall('./job/sequence/command/node-step-plugin/configuration/entry'):
      if entry.attrib['key'] == 'destinationPath':
        entry.set('value',job["VNF Container"])
      elif entry.attrib['key'] == 'sourcePath':
        entry.set('value',job["VNF Folder"] + job["Event"] + '.' + job["Template File Format"])
  else:
    for command in root.findall('./job/sequence/command'):
      if command.find('node-step-plugin') is not None:
        root.find('./job/sequence').remove(command)
  if "Command" in job:
    root.find('./job/sequence/command/exec').text = job["Command"]
    root.find('./job/context/project').text = vnf_id
  else:
    for command in root.findall('./job/sequence/command'):
      if command.find('exec') is not None:
        root.find('./job/sequence').remove(command)
#  if notification:
#    root.find('./job/notification/onfailure/webhook').set('urls','http://192.168.1.1/panic/')
#    root.find('./job/notification/onsuccess/webhook').set('urls','http://192.168.1.1/victory/')
#  else:
  root[0].remove(root.find('./job/notification'))
  root.find('./job/name').text = job["Event"]
  tree.write("job_temp.xml")
  job_url = post_job("job_temp.xml")
  return job_url

def execute_job():
  pass
