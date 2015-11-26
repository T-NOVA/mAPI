from bottle import route, run, auth_basic, request, abort, parse_auth
from Config.configuration import Configuration
from registerVNF import register_vnf
from requestDispatcher import get_current_configuration, initial_configuration, update_configuration, delete_vnf
from json import loads
from Database.mapidb import mapiDB
import httplib

conf = Configuration()
db = mapiDB()
auth_method = conf.get_authentication_method()
if auth_method == 'gatekeeper':
  gatekeeper_host = conf.get_gk_host()
  gatekeeper_port = conf.get_gk_host()
  service_key = conf.get_gk_key()
if str(auth_method) == 'basic':
  username = conf.get_username()
  password = conf.get_password()

def validate_VNF(vnf_id):
  if db.get_VNF(str(vnf_id)) == None:
    return False
  else:
    return True

def check_credentials(user, passwd):
  print user, passwd
  if user == username and passwd == password:
    return True
  else:
    return False

def gatekeeper_authentication(token):
  con = httplib.HTTPConnection(gatekeeper_host, gatekeeper_port)
  headers = ({"Content-Type":"application/json",
             "X-Auth-Service-Key":"%s" % service_key})
  con.request('POST', '/token/validate/' + token, headers = headers)
  response = con.getresponse().read()
  if response.status == '200':
    return True
  else:
    return False


@route('/vnf_api/', method = 'POST')
def api_registervnf():
  if auth_method == 'gatekeeper':
    print 'gatekeeper'
    if not gatekeeper_authentication(request.get_header('X-Auth-Token')):
      abort(401)
  if auth_method == 'basic':
    print 'basic authentication method'
    user, passwd = parse_auth(request.get_header('Authorization'))
    if not check_credentials(user, passwd):
      abort(401)
  try:
    vnfd = loads(request.body.getvalue())
    print "\n######## REGISTERING VNF ########\n"
    print "VNF Id: " + vnfd['id'] + '\n'
    print "VNF Descriptor: "
    print vnfd
    register_vnf(vnfd['id'], vnfd)
    print "\n############## END ##############\n"
  except:
    abort(400)

@route('/vnf_api/<vnf_id>/config/', method = 'GET')
def api_get_vnf_config(vnf_id):
  if auth_method == 'gatekeeper':
    if not gatekeeper_authentication(request.get_header('X-Auth-Token')):
      abort(401)
  elif auth_method == 'basic':
    user, passwd = parse_auth(request.get_header('Authorization'))
    if not check_credentials(user, passwd):
      abort(401)
  print "\n######## RETRIEVE VNF CURRENT CONFIGURATION ########\n"
  print "VNF Validation: "
  if validate_VNF(vnf_id):
    print "Ok"
    print "\nRetrieve Configuration workflow \n"
    conf_obj = get_current_configuration(vnf_id)
    if not conf_obj:
      print "\nThe VNF has not been configured\n"
      print "\n############## END ##############\n"
      abort(404)
    else:
      print "\n############## END ##############\n"
      return conf_obj
  else:
    print "Fail: VNF not found"
    print "\n############## END ##############\n"
    abort(404) 

@route('/vnf_api/<vnf_id>/config/', method = 'POST')
def api_vnf_init_config(vnf_id):
  if auth_method == 'gatekeeper':
    if not gatekeeper_authentication(request.get_header('X-Auth-Token')):
      abort(401)
  elif auth_method == 'basic':
    user, passwd = parse_auth(request.get_header('Authorization'))
    if not check_credentials(user, passwd):
      abort(401)
  print "\n######## VNF INITIAL CONFIGURATION ########\n"
  print "VNF Validation: "
  if validate_VNF(vnf_id):
    print "Ok"
    print "\nRetrieving VNF Configuration: \n"
    try:
      vnfm_request = loads(request.body.getvalue())
      print vnfm_request
    except:
      print "Fail: Unable to retrieve VNF Configuration"
      print "\n############## END ##############\n"
      abort(400)
    finally:
      print "\nStarting VNF initial configuration workflow\n"
      response = initial_configuration(vnf_id, vnfm_request)
      if not response:
        print "Fail: Unable to configure VNF"
        print "\n############## END ##############\n"
        abort(500)
  else:
    print "Fail: VNF not found"
    print "\n############## END ##############\n"
    abort(404)

@route('/vnf_api/<vnf_id>/config/', method = 'PUT')
def api_vnf_update_config(vnf_id):
  if auth_method == 'gatekeeper':
    if not gatekeeper_authentication(request.get_header('X-Auth-Token')):
      abort(401)
  elif auth_method == 'basic':
    user, passwd = parse_auth(request.get_header('Authorization'))
    if not check_credentials(user, passwd):
      abort(401)
  print "\n######## UPDATE VNF CONFIGURATION ########\n"
  print "VNF Validation: "
  if validate_VNF(vnf_id):
    print "Ok"
    print "\nRetrieving VNF Configuration: \n"
    try:
      vnfm_request = loads(request.body.getvalue())
      print vnfm_request
    except:
      print "Fail: Unable to retrieve VNF Configuration"
      print "\n############## END ##############\n"
      abort(400)
    finally:
      print "\nStarting VNF Configuration Workflow\n"
      response = update_configuration(vnf_id, vnfm_request)
  else:
    print "Fail: VNF not found"
    print "\n############## END ##############\n"
    abort(404)

@route('/vnf_api/<vnf_id>/', method = 'DELETE')
def api_delete_vnf(vnf_id):
  if auth_method == 'gatekeeper':
    if not gatekeeper_authentication(request.get_header('X-Auth-Token')):
      abort(401)
  if auth_method == 'basic':
    print "basic authentication"
    user, passwd = parse_auth(request.get_header('Authorization'))
    if not check_credentials(user, passwd):
      abort(401)
  print "\n######## DELETE VNF CONFIGURATION API ########\n"
  print "VNF Validation: "
  if validate_VNF(vnf_id):
    print "Ok\n"
    try:
      vnfm_request = loads(request.body.getvalue())
    except:
      vnfm_request = None
    finally:
      print "\nStarting VNF removal workflow\n"
      response = delete_vnf(vnf_id, vnfm_request)
      if not response:
        print "Fail: the VNF could not be removed\n"
        print "\n############## END ##############\n"
        abort(500)
      print "\n############## END ##############\n"
  else:
    print "Fail: VNF not found"
    print "\n############## END ##############\n"
    abort(404)

run(host = conf.get_server_ip(), port = conf.get_server_port(), reloader=True)
