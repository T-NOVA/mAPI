
class keyFixer(object):

  def __init__(self, mapi_folder, vnf_id, key):
    self.path = mapi_folder + "keys/" + vnf_id + ".pem"
    self.key = key
    self.lineS = '-----BEGIN RSA PRIVATE KEY-----'
    self.lineE = '-----END RSA PRIVATE KEY-----'

  def parseKey(self):
    content = self.key.split(self.lineS)[1].split(self.lineE)[0]
    key_file = open(self.path, 'w')
    print >> key_file, self.lineS
    for x in range(0,len(content),64):
      print >> key_file, content[x:x+64]
    print >> key_file, self.lineE
    key_file.close()
    del(content)
    del(key_file)
