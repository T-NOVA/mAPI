from mapidb_declarative import Base, VNF, Event
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Config import configuration

def create_session():
  conf = configuration.Configuration()
  db_user, db_password, db_ip = conf.get_db_parameters()
  engine = create_engine('mysql://' + db_user + ':' + db_password + '@' + db_ip + '/mapi')
  Base.metadata.bind = engine 
  DBSession = sessionmaker(bind=engine)
  session = DBSession()
  return session 

class mapiDB(object):
  def __init__(self):
    self.session = create_session()

  def add_VNF(self, vnf_id, project_url):
    self.session.add(VNF(id = vnf_id, projectUrl = project_url))
    self.session.commit()
    return self.session.query(VNF).filter_by(id = vnf_id).first()

  def get_VNF(self, vnf_id):
    return self.session.query(VNF).filter_by(id = vnf_id).first()

  def delete_VNF(self, vnf):
    self.session.delete(vnf)
    self.session.commit()

  def add_event(self, name, job_url, vnf):
    self.session.add(Event(name = name, jobUrl = job_url, vnf = vnf))
    self.session.commit()

  def get_event(self, event_name, vnf):
    return self.session.query(Event).filter(Event.name == event_name).filter(Event.vnfId == vnf).one()

  def get_all_events(self, vnf):
    return self.session.query(Event).filter(Event.vnfId == vnf).all()

  def delete_event(self, event):
    self.session.delete(event)
    self.session.commit()
