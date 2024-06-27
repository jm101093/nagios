#!/omd/sites/node/bin/python

### Version 2.0
### Added runnign from Proxy feature by passing config file name as argument

import urllib2, sys, os, socket, pprint, json, getopt

opt_debug = '--debug' in sys.argv

def fetch_var(server, port, suburi, target, targetuser, targetpwd, path, attb, lpath, itemspec):
#   sys.stdout.write("%s %s %s %s %s %s %s %s \n" % (server, port, target, targetuser, targetpwd, path, suburi, itemspec))
    if not path:
	query_args = {"type":"READ","target":{"url":target,"user":targetuser,"password":targetpwd},"mbean":"java.lang:*,type=Runtime","attribute":"Name,SpecVendor,SpecVersion"}
#	query_args = {"type":"READ","target":{"url":target,"user":targetuser,"password":targetpwd}}
    else:
        if not attb:
#		sys.stdout.write("attribute is %s\n" % (attb))
		query_args = {"type":"READ","target":{"url":target,"user":targetuser,"password":targetpwd},"mbean":path}
	else:
#	  sys.stdout.write("attribute is here %s\n" % (attb))
	  if not lpath:
		try:	
			query_args = {"type":"READ","target":{"url":target,"user":targetuser,"password":targetpwd},"mbean":path,"attribute":attb}
		except Exception, e:
	        	sys.stderr.write("ERROR: %s" % e)
	        	return []
	  else:
                try:
                        query_args = {"type":"READ","target":{"url":target,"user":targetuser,"password":targetpwd},"mbean":path,"attribute":attb,"path":lpath}
                except Exception, e:
                        sys.stderr.write("ERROR: %s" % e)
                        return []
    url = "http://%s:%d/%s" % (server, port, suburi)
#   sys.stdout.write("%s \n" % (url))
#   sys.stdout.write("%s \n" % (query_args))
    try:
        json1 = urllib2.urlopen(url,json.dumps(query_args),10).read()
    except Exception, e:
        sys.stderr.write("ERROR: %s" % e)
        return []

    try:
        true = True
        false = False
        null = None
        obj = eval(json1)
    except Exception, e:
        sys.stderr.write('ERROR: Invalid json code (%s)\n' % e)
        sys.stderr.write('       Response %s\n' % json1)
        return []

    if obj.get('status', 200) != 200:
        sys.stderr.write('ERROR: Invalid response when fetching url %s\n' % url)
        sys.stderr.write('       Response: %s\n' % json1)
        return []

    # Only take the value of the object. If the value is an object
    # take the first items first value.
    # {'Catalina:host=localhost,path=\\/test,type=Manager': {'activeSessions': 0}}
    if 'value' not in obj: 
        if opt_debug:
            sys.stderr.write("ERROR: not found: %s\n" % path)
        return []
    val = obj.get('value', None)
    return make_item_list((), val, itemspec)

# convert single values into lists of items in
# case value is a 1-levelled or 2-levelled dict
def make_item_list(path, value, itemspec):
    if type(value) != dict:
        if type(value) == str:
            value = value.replace(r'\/', '/')
        return [(path, value)]
    else:
        result = []
        for key, subvalue in value.items():
            # Handle filtering via itemspec
            miss = False
            while itemspec and '=' in itemspec[0]:
                if itemspec[0] not in key:
                    miss = True
                    break
                itemspec = itemspec[1:]
            if miss:
                continue
            item = extract_item(key, itemspec)
            if not item:
                item = (key,)
            result += make_item_list(path + item, subvalue, [])
        return result

# Example:
# key = 'Catalina:host=localhost,path=\\/,type=Manager'
# itemsepc = [ "path" ]
# --> "/"

def extract_item(key, itemspec):
    path = key.split(":", 1)[-1]
    components = path.split(",")
    item = ()
    comp_dict = {}
    for comp in components:
        parts = comp.split("=")
        if len(parts) == 2:
            left, right = parts
            comp_dict[left] = right
    for pathkey in itemspec:
        if pathkey in comp_dict:
            right = comp_dict[pathkey]
            right = right.replace(r'\/', '/')
            right = right.replace(r' ', '_')
            if '/' in right:
                right = '/' + right.split('/')[-1]
            item = item + (right,)
    return item


def query_instance(inst):
    # Prepare user/password authentication via HTTP Auth
    if inst.get("password"):
        passwdmngr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passwdmngr.add_password(None, "http://%s:%d/" % 
                (inst["server"], inst["port"]), inst["user"], inst["password"])
        if inst["mode"] == 'digest':
            authhandler = urllib2.HTTPDigestAuthHandler(passwdmngr)
        else:
            authhandler = urllib2.HTTPBasicAuthHandler(passwdmngr)
        opener = urllib2.build_opener(authhandler)
        urllib2.install_opener(opener)

    sys.stdout.write('<<<megen_info>>>\n')
##Determine type of server
##  server_info = fetch_var(inst["server"], inst["port"], inst["target"], inst["targetuser"], inst["targetpwd"], "", inst["suburi"], "")
    try:
 	    server_info = fetch_var(inst["server"], inst["port"], inst["suburi"], inst["target"], inst["targetuser"], inst["targetpwd"], "", "", "", "")
    except Exception, e:
            sys.stderr.write("ERROR: %s" % e)
            return []
##  sys.stdout.write('<<<jboss_info>>>\n')
    if server_info:
       d = dict(server_info)
##     version = d.get(('info', 'version'), "unknown")
       version = (d.get(('java.lang:type=Runtime','SpecVersion'), "unknown"))
##     product = d.get(('info', 'product'), "unknown")
       product = (d.get(('java.lang:type=Runtime','SpecVendor'), "unknown")).replace(' ','_')
##     agentversion = d.get(('agent',), "unknown")
##     agentversion = d.get(('jboss.management.local:j2eeType=JVM,name=Local','javaVersion'), "unknown")
       name = (d.get(('java.lang:type=Runtime','Name'), "unknown"))

       sys.stdout.write("%s %s %s %s\n" % (inst["instance"], name, product, version))
    else:
##     sys.stdout.write("%s ERROR\n" % (inst["instance"],))
       return

    sys.stdout.write('<<<megen_metrics>>>\n')
    # Fetch the general information first
    product = "megen"
#   sys.stdout.write("%s %s %s %s\n" % (inst["instance"], product, version, agentversion))
    for path, attribute, lpath, title, itemspec in global_vars + specific_vars.get(product, []):
    
#       sys.stdout.write("%s %s %s %s %s %s %s %s %s\n" % (inst["server"], inst["port"], inst["suburi"], inst["target"], inst["targetuser"], inst["targetpwd"], path, attribute, itemspec))
        try:
            values = fetch_var(inst["server"], inst["port"], inst["suburi"], inst["target"], inst["targetuser"], inst["targetpwd"], path, attribute, lpath, itemspec)

        # In case of network errors skip this server
        except IOError:
            return
        except socket.timeout:
            return
        except:
            if opt_debug:
                raise
            # Simply ignore exceptions. Need to be removed for debugging
            continue
    
        for subinstance, value in values:
            if not subinstance and not title:
                print "INTERNAL ERROR: %s" % value
                continue

            if len(subinstance) > 1:
                item = ",".join((inst["instance"],) + subinstance[:-1])
            else:
                item = inst["instance"]
            if title:
                if subinstance:
                    tit = title + "." + subinstance[-1]
                else:
                    tit = title
            else:
                tit = subinstance[-1]

            sys.stdout.write("%s %s %s\n" % (item, tit, value))


# Default configuration for all instances
server   = "localhost"
port     = 8080
user     = "youuser"
password = "yourpass"
mode     = "digest"
suburi   = "jolokia"
target   = None
targetuser = None
targetpwd = None
instance = None


global_vars = [
# ( "java.lang:type=Memory",	"NonHeapMemoryUsage",	"used",	"NonHeapMemoryUsage",      [] ),
# ( "java.lang:type=Memory",    "NonHeapMemoryUsage",	"max",	"NonHeapMemoryMax",        [] ),
# ( "java.lang:type=Memory",    "HeapMemoryUsage",	"used",	"HeapMemoryUsage",         [] ),
# ( "java.lang:type=Memory",    "HeapMemoryUsage",   	"max",	"HeapMemoryMax",           [] ),
# ( "java.lang:type=Threading", "ThreadCount",		None,	"ThreadCount",             [] ),	
# ( "java.lang:type=Threading", "DaemonThreadCount",	None,	"DeamonThreadCount",	   [] ),
# ( "java.lang:type=Threading", "PeakThreadCount",      None,	"PeakThreadCount",   	   [] ),
# ( "java.lang:type=Threading", "TotalStartedThreadCount", None,"TotalStartedThreadCount", [] ),
# ( "java.lang:type=Runtime",   "Uptime",		None,	"Uptime",                  [] ),
]


specific_vars = {
  "weblogic" : [
      ( "*:*/CompletedRequestCount",                          None,                      [ "ServerRuntime" ] ),
      ( "*:*/QueueLength",                                    None,                      [ "ServerRuntime" ] ),
      ( "*:*/StandbyThreadCount",                             None,                      [ "ServerRuntime" ] ),
      ( "*:*/PendingUserRequestCount",                        None,                      [ "ServerRuntime" ] ),
      ( "*:Name=ThreadPoolRuntime,*/ExecuteThreadTotalCount", None,                      [ "ServerRuntime" ] ),
      ( "*:*/ExecuteThreadIdleCount",                         None,                      [ "ServerRuntime" ] ),
      ( "*:*/HoggingThreadCount",                             None,                      [ "ServerRuntime" ] ),
      ( "*:Type=WebAppComponentRuntime,*/OpenSessionsCurrentCount", None,                [ "ServerRuntime", "ApplicationRuntime" ] ),
  ],
  "tomcat" : [
      ( "*:type=Manager,*/activeSessions,maxActiveSessions",  None,                      [ "path", "context" ] ),
      ( "*:j2eeType=Servlet,name=default,*/stateName", None, [ "WebModule" ] ),
      # Check not yet working
      ( "*:j2eeType=Servlet,name=default,*/requestCount", None, [ "WebModule" ]),

     # too wide location for addressing the right info
     # ( "*:j2eeType=Servlet,*/requestCount", None, [ "WebModule" ] ),

  ],
  "jboss" : [
#     ( "*:type=Manager,*", "activeSessions,maxActiveSessions",  None,                      [ "path", "context" ] ),
#     ( None, 					None, None,   		                   [] ), 
#     ( "org.hornetq:module=JMS,*,type=Queue",  None, None,             		   ["name" ] ),
      ( "org.hornetq:module=JMS,*,type=Queue",	"MessageCount",	None,	None,                      ["name" ] ),
  ],
  "megen" : [
      ( "com.mitchell.eventgenerator:EventGeneratorId=*,*,Id=JobMetrics,type=Job",  "NumCompletedEvents,NumFailedEvents,NumAcknowledgedFailedEvents,NumScansWithErrors,NumAcknowledgedScansWithErrors,NumScans,NumFailedScans,NumAcknowledgedFailedScans,Status", None,   None,                      [ "Group", "EventGeneratorId" ] ),
      ( "com.mitchell.eventgenerator:EventGeneratorId=*,*,Id=Admin,type=Job",  "Status", None,   None,                      [ "Group", "EventGeneratorId" ] ),
#     ( "com.mitchell.eventgenerator:EventGeneratorId=*,*,Id=JobMetrics,type=Job",  "NumEmptyScans", None,   None,                      ["Group", "EventGeneratorId" ] ),
#     ( "com.mitchell.eventgenerator:EventGeneratorId=*,*,Id=JobMetrics,type=Job",  "NumFailedScans", None,   None,                      ["Group", "EventGeneratorId" ] ),
  ],
}


#   ( '*:j2eeType=WebModule,name=/--/localhost/-/%(app)s,*/state', None, [ "name" ]),
#   ( '*:j2eeType=Servlet,WebModule=/--/localhost/-/%(app)s,name=%(servlet)s,*/requestCount', None, [ "WebModule", "name" ]),
#   ( "Catalina:J2EEApplication=none,J2EEServer=none,WebModule=*,j2eeType=Servlet,name=*", None, [ "WebModule", "name" ]),


# List of instances to monitor. Each instance is a dict where
# the global configuration values can be overridden.
instances = [{}]

conffile = os.getenv("MK_CONFDIR", "/home/sitescope/check_mk_agent/etc") + "/megen.cfg" 
opts, args = getopt.getopt(sys.argv[1:], "m:d", ["debug", "megen="])
for o, a in opts:
 if o in ("m", "--megen"):
  conffile = os.getenv("MK_CONFDIR", "/home/sitescope/check_mk_agent/etc") + "/" + a

if instance == None:
    instance = str(port)

if os.path.exists(conffile):
    execfile(conffile)


# We have to deal with socket timeouts. Python > 2.6
# supports timeout parameter for the urllib2.urlopen method
# but we are on a python 2.5 system here which seem to use the
# default socket timeout. We are local here so  set it to 1 second.
socket.setdefaulttimeout(1.0)

# Compute list of instances to monitor. If the user has defined
# instances in his configuration, we will use this (a list
# of dicts).
for inst in instances:
    for varname, value in [
        ( "server", server ),
        ( "port", port ),
        ( "user", user ),
        ( "password", password ),
        ( "mode", mode ),
        ( "suburi", suburi ),
        ( "target", target),
        ( "targetuser", targetuser ),
        ( "targetpwd", targetpwd ),
        ( "instance", instance )]:
        if varname not in inst:
            inst[varname] = value
    if not inst["instance"]:
        inst["instance"] = str(inst["port"])
    inst["instance"] = inst["instance"].replace(" ", "_")

    query_instance(inst)



