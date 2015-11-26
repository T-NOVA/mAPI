import json

def enrich_config_template(vnfm_request, template):
  print "\nCREATING CONFIG FILE OBJECT\n"
  print "Request sent by VNF Manager: "
  print vnfm_request
  print "Template created by VNF developer: "
  print template
  for key in vnfm_request.keys():
    print "Key in VNF Manager request: " + key
    for item in template.iteritems():
      if item[1] == "get_attr"+str([elem.encode('ascii','ignore') for elem in key.split('_')]).translate(None,"' "):
        print "Found Key"
        template.update({item[0]:vnfm_request.get(key)[0]})
  print "\nConfiguration file complete!"
  return template
