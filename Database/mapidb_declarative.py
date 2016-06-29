from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from Config import configuration

conf = configuration.Configuration()
db_user, db_password, db_ip = conf.get_db_parameters()

Base = declarative_base()

class VNF(Base):
  __tablename__ = 'VNFs'

  id = Column(String(64), primary_key = True)
  projectUrl = Column(String(100))
  username = Column(String(100))
#  events = relationship("Event", backref = 'VNFs', cascade = "all,delete")

  def __repr__(self):
    return "<VNF (VNF Id='%s', Project URL='%s', VNF Username='%s')>" %(self.id, self.projectUrl, self.username)

class Event(Base):
  __tablename__ = 'Events'

  id = Column(Integer, primary_key = True)
  name = Column(String(64))
  jobUrl = Column(String(100))
  vnfId = Column(String(64), ForeignKey('VNFs.id'))
  
  vnf = relationship("VNF", backref=backref('events', order_by=id, cascade ="all, delete"))

  def __repr__(self):
    return "Event (Event Name='%s', Job Url='%s', VNF Id='%s')>" %(self.name, self.jobUrl, self.vnfId)

engine = create_engine('mysql://' + db_user + ':' + db_password + '@' + db_ip + '/mapi', pool_recycle = 300)

Base.metadata.create_all(engine)
