import xml.etree.cElementTree as ET
import httplib
from json import loads, dumps
from Auxiliary import formdata
from Config import configuration
import sys

conf = configuration.Configuration()
mapi_folder = conf.get_mAPI_folder()
rundeck_host = conf.get_rundeck_host()
rundeck_port = conf.get_rundeck_port()
rundeck_token = conf.get_rundeck_token()
rundeck_project_folder = conf.get_rundeck_project_folder()

def is_job_running(jobId):
  print "\nChecking if Job is still running"
  print jobId
  con = httplib.HTTPConnection(rundeck_host, rundeck_port)
  headers = ({"Content-Type":"application/json",
             "X-Rundeck-Auth-Token":"%s" % rundeck_token})
  con.request('GET', '/api/12/job/'+jobId+'/executions?status=running', headers = headers)
  response = ET.fromstring(con.getresponse().read())
  if response.get("count") == '0':
    return False
  else:
    return True

def post_project(file_as_text):
  print "\nProject request which will be upload to Rundeck: \n"
  print file_as_text
  con = httplib.HTTPConnection(rundeck_host, rundeck_port)
  headers = ({"Content-Type":"application/json",
             "X-Rundeck-Auth-Token":"%s" % rundeck_token})
  con.request('POST', '/api/12/projects', file_as_text, headers = headers)
  response = con.getresponse().read()
  print "\nRundeck Response: \n"
  print response
  print "\nFinished uploading project to Rundeck\n"
  return loads(response)['url']

def post_job(filename):
  print "\nUploading Job to Rundeck\n"
  files = {'xmlBatch': {'filename': filename, 'content': open(filename,'rb').read()}}
  data, headers = formdata.encode_multipart({}, files)
  con = httplib.HTTPConnection(rundeck_host, rundeck_port)
  headers["X-Rundeck-Auth-Token"] = "%s" % rundeck_token
  con.request('POST', '/api/12/jobs/import/', data, headers = headers)
  response = con.getresponse()
  xml = ET.fromstring(response.read())
  print "\nFinished uploading Job to Rundeck\n"
  return xml.find('./succeeded/job').attrib['href']

def delete_project(project_url):
  print "\nDeleting project from Rundeck\n"
  print "Project URL: " + project_url
  con = httplib.HTTPConnection(rundeck_host, rundeck_port)
  headers = ({"X-Rundeck-Auth-Token" : "%s" % rundeck_token})
  con.request('DELETE', project_url, headers = headers)
  response = con.getresponse()
  status, msg = response.status, response.read()
  print "\nRundeck response: " + str(status) +'\n' + str(msg)
  print "\nFinished deleting project from Rundeck\n"
  return status

def delete_job(job_url):
  print "\nDeleting Job " + job_url + "from Rundeck\n"
  con = httplib.HTTPConnection(rundeck_host, rundeck_port)
  headers = ({"X-Rundeck-Auth-Token" : "%s" % rundeck_token})
  con.request('DELETE', job_url, headers = headers)
  print "\nFinished deleting job from Rundeck\n"

def create_project(vnf_id, ems):
  print "\nCreating project in Rundeck\n"
  print mapi_folder
  with open(mapi_folder + 'Rundeck_Aux/project_request.json', 'r') as f:
    project_request = loads(f.read())
  print project_request
  project_request['name'] = vnf_id
  if ems['driver'].lower() == 'ssh':
    if ems['authentication_type'] == 'PubKeyAuthentication':
      project_request['config']['project.ssh-keypath'] = mapi_folder + 'keys/' + vnf_id + '.pem'
  response = post_project(dumps(project_request))
  print "\nFinished Creating project in Rundeck\n"
  return response

def add_node(vnf_id, ip_address, vnf_username):
  print "\nAdding Node to Rundeck: \n"
  print "VNF ID: " + vnf_id + '\n'
  print "IP Address: " + ip_address + '\n'
  print "Username :" + vnf_username + '\n'
  project = ET.Element("project")
  ET.SubElement(project, "node", name="vnf-mgmt", description="vnf management element", tags="vnf-mgmt", hostname=ip_address,osFamily="unix", username=vnf_username)
  ET.ElementTree(project).write(rundeck_project_folder + vnf_id + "/etc/resources.xml", encoding="UTF-8", xml_declaration=True)
  print "\nFinished adding node to Rundeck\n"

def update_job(job_id, ip, project):
  print "\nUpdating Job\n"
  print "job id: "+job_id
  print "VNFC ip: "+ip

  job = get_job(job_id)
  root = ET.fromstring(job)

  # update only HTTP commands
  for command in root.findall('./job/sequence/command'):
      if command.find('node-step-plugin') is not None:
        if command.find('node-step-plugin').attrib['type'] != 'httpCommandNodeStep':
          print "No need for update"
          return 0
      else:
        print "No need for update"
        return 0

  for entry in root.findall('./job/sequence/command/node-step-plugin/configuration/entry'):
    if entry.attrib['key'] == 'url':
      entry.set('value','http://'+ip+entry.attrib['value'])
      print entry.attrib['key'] + entry.attrib['value']

  tree = ET.ElementTree(root)
  tree.write("job_temp.xml")

  print "\nUpdating Job in Rundeck\n"
  files = {'xmlBatch': {'filename': "job_temp.xml", 'content': open("job_temp.xml",'rb').read()}}
  data, headers = formdata.encode_multipart({"dupeOption":"update", "project": project}, files)
  con = httplib.HTTPConnection(rundeck_host, rundeck_port)
  headers["X-Rundeck-Auth-Token"] = "%s" % rundeck_token
  con.request('POST', '/api/12/jobs/import/', data, headers = headers)
  response = con.getresponse()
  xml = ET.fromstring(response.read())
  print "\nFinished uploading Job to Rundeck\n"
  return xml.find('./succeeded/job').attrib['href']

def create_job(vnf_id, job):
  print "\nCreate Job in Rundeck\n"
  print "Job description: \n"
  print job

  if job['authentication_type'] == 'HTTPBasicAuth':
    tree = ET.parse(mapi_folder + 'Rundeck_Aux/http_job_template.xml')
    root = tree.getroot()

    for command in root.findall('./job/sequence/command'):
      if command.find('node-step-plugin') is not None:
        print command.tag, command.attrib
        if command.find('node-step-plugin').attrib['type'] == 'httpUploadNodeStep':
          root.find('./job/sequence').remove(command)
          print 'delete command'

    for entry in root.findall('./job/sequence/command/node-step-plugin/configuration/entry'):
      request = job["command"].split()
      if entry.attrib['key'] == 'method':
        entry.set('value',request[0])
      elif entry.attrib['key'] == 'url':
        if job["authentication_port"] != "80":
          entry.set('value',":"+job["authentication_port"]+request[1])
        else:
          entry.set('value',request[1])
      elif entry.attrib['key'] == 'user':
        entry.set('value',job["authentication_username"])
      elif entry.attrib['key'] == 'password':
        entry.set('value',job["authentication"])

    root.find('./job/context/project').text = vnf_id
  else:
    tree = ET.parse(mapi_folder + 'Rundeck_Aux/job_template.xml')
    root = tree.getroot()
    if "template_file" in job:
      for entry in root.findall('./job/sequence/command/node-step-plugin/configuration/entry'):
        if entry.attrib['key'] == 'destinationPath':
          entry.set('value',job["VNF Container"])
        elif entry.attrib['key'] == 'sourcePath':
          entry.set('value',job["VNF Folder"] + 'current' + '.' + job["template_file_format"].lower())
    else:
      for command in root.findall('./job/sequence/command'):
        if command.find('node-step-plugin') is not None:
          root.find('./job/sequence').remove(command)
    if "command" in job:
      root.find('./job/sequence/command/exec').text = job["command"]
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
  #print ET.tostring(root)
  job_url = post_job("job_temp.xml")
  print "\nJob is available at: " + job_url
  print "\nFinished creating job in Rundeck\n"
  return job_url

def execute_job(jobUrl):
  print "\nExecuting job in Rundeck\n"
  print "Job url: " + jobUrl
  con = httplib.HTTPConnection(rundeck_host, rundeck_port)
  headers = ({"Content-Type":"application/json",
             "X-Rundeck-Auth-Token":"%s" % rundeck_token})
  con.request('POST', jobUrl+'/run', headers = headers)
  response = con.getresponse().read()
  print "\nFinished executing job in Rundeck\n"
  return response

def list_jobs(project_id):
  print "\nListing jobs\n"
  print "Project: " + project_id
  con = httplib.HTTPConnection(rundeck_host, rundeck_port)
  headers = ({"X-Rundeck-Auth-Token" : "%s" % rundeck_token})
  con.request('GET', '/api/12/project/'+project_id+'/jobs', headers = headers)
  response = con.getresponse().read()
  #print response
  print "\nFinished listing jobs\n"
  return response

def get_job(job_id):
  print "\nGet job\n"
  print "Job: "+job_id
  con = httplib.HTTPConnection(rundeck_host, rundeck_port)
  headers = ({"X-Rundeck-Auth-Token" : "%s" % rundeck_token})
  con.request('GET', '/api/12/job/'+job_id, headers = headers)
  response = con.getresponse().read()
  #print response
  print "\nFinish getting job\n"
  return response