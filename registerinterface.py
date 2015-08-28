from bottle import route, run, auth_basic, request
from Config.configuration import Configuration
from registerVNF import register_vnf
from json import loads

conf = Configuration()

def check_credentials(user, passwd):
  if user == conf.get_username() and passwd == conf.get_password():
    return True
  else:
    return False

@route('/vnf_api/', method = 'POST')
@auth_basic(check_credentials)
def registervnf():
  vnfd = loads(request.body.getvalue())
  print vnfd
  print vnfd['id']

  register_vnf(vnfd['id'], vnfd)

run(host = conf.get_server_ip(), port = conf.get_server_port(), reloader=True)
