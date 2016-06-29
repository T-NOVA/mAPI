import MySQLdb as sql
from Config import configuration

class VNF(object):
  
  def __init__(self, id, projectUrl, username):
    self.id = id
    self.projectUrl = projectUrl
    self.username = username
    self.events = []

  def associateEvents(self, event_list):
    self.events = event_list

class Event(object):

  def __init__(self, id, name, jobUrl, vnfId):
    self.id = id
    self.name = name
    self.jobUrl = jobUrl
    self.vnfId = vnfId

  def associateVnf(self, vnf_obj):
    self.vnf = vnf_obj

def open_connection():
  conf = configuration.Configuration()
  db_user, db_password, db_ip = conf.get_db_parameters()
  con = sql.connect(db_ip, db_user , db_password, 'mapi')
  cur = con.cursor(sql.cursors.DictCursor)
  return con,cur

def add_VNF(vnf_id, projectUrl, username):
  con, cur = open_connection()
  try:
    vnf_obj = VNF(vnf_id, projectUrl, username)
    cur.execute("insert into VNFs(id, projectUrl, username) values(%s,%s,%s)", (vnf_id, projectUrl, username))
    con.commit()
    return vnf_obj
  finally:
    con.close()

def get_VNF(vnf_id):
  con, cur = open_connection()
  try:
    cur.execute("select * from VNFs where id = '" + str(vnf_id) + "'")
    res = cur.fetchone()
    vnf =  VNF(vnf_id, res['projectUrl'], res['username'])
    vnf.associateEvents(get_all_events(vnf))
    if res:
      return vnf
    else:
      return None
  finally:
    con.close()

def delete_VNF(vnf_obj):
  con, cur = open_connection()
  try:
    event_list = get_all_events(vnf_obj)
    for event in event_list:
      delete_event(event)
    cur.execute("delete from VNFs where id = '" + str(vnf_obj.id) + "'")
    con.commit()
  finally:
    con.close()

def add_event(name, job_url, vnf_obj):
  con, cur = open_connection()
  try:
    cur.execute("insert into Events(name, jobUrl, vnfId) values(%s,%s,%s)", (name, job_url, vnf_obj.id))
    con.commit()
    cur.execute("select LAST_INSERT_ID() from Events")
    res = cur.fetchone()["LAST_INSERT_ID()"]
    event = Event(res, name, job_url, vnf_obj.id)
    event.associateVnf(get_VNF(vnf_obj.id))
    return event
  finally:
    con.close()

def get_event(event_name, vnf_obj):
  con, cur = open_connection()
  try:
    cur.execute("select * from Events where vnfId = '" + str(vnf_obj.id) + "' and name = '" + str(event_name) + "'")
    res = cur.fetchone()
    if res:
      event = Event(res['id'], res['name'], res['jobUrl'], res['vnfId'])
      event.associateVnf(get_VNF(vnf_obj.id))
      return event
    else: 
      return None
  finally:
    con.close()

def get_all_events(vnf_obj):
  con, cur = open_connection()
  try:
    cur.execute("select * from Events where vnfId = '" + str(vnf_obj.id) + "'")
    res = cur.fetchall()
    event_list = []
    if res:
      for elem in res:
        event_list.append(Event(elem['id'], elem['name'], elem['jobUrl'], elem['vnfId']))
      return event_list
    else: 
      return event_list
  finally:
    con.close()

def delete_event(event_obj):
  con, cur = open_connection()
  try:
    cur.execute("delete from Events where id = '" + str(event_obj.id) + "'")
    con.commit()
  finally:
    con.close()

