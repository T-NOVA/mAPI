from ConfigParser import RawConfigParser


class Configuration(object):
  def __init__(self):
    self.config = RawConfigParser()
    self.config.read('./Config/mAPI.cfg')

  def get_username(self):
    return self.config.get('authentication', 'username') 

  def get_password(self):
    return self.config.get('authentication', 'password')

  def get_server_ip(self):
    return self.config.get('server', 'ip')

  def get_server_port(self):
    return self.config.get('server', 'port')

  def get_mAPI_folder(self):
    return self.config.get('general', 'folder')

  def get_rundeck_host(self):
    return self.config.get('rundeck', 'host')

  def get_rundeck_port(self):
    return self.config.get('rundeck', 'port')

  def get_rundeck_token(self):
    return self.config.get('rundeck', 'token')

  def get_rundeck_project_folder(self):
    return self.config.get('rundeck', 'project_folder')

  def get_db_parameters(self):
    return self.config.get('db','user'), self.config.get('db','password'), self.config.get('db','ip')
