#
# setPorts.py
# Author: Bob Clarke
# Date: 04/03/2014
#

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Setup
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import sys;

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Functions
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def modPorts ( cName,startPort ):

	# Get a list of hostnames
	dict = {}
	for node in AdminConfig.list('Node').split():
    		nHost = AdminConfig.showAttribute(node, 'hostName')
    		nName = AdminConfig.showAttribute(node, 'name')

    	# Tie the hostname to the nodename and store in a hashtable for later use
    	dict[nName] = nHost
  	try:

    		clusterId=AdminConfig.getid('/Cell:'+cellName+'/ServerCluster:'+cName)
    		members=AdminConfig.list('ClusterMember',clusterId).splitlines()
    		for member in members :
      			sPort = startPort
      			nodeName=AdminConfig.showAttribute(member,"nodeName")
      			memberName=AdminConfig.showAttribute(member,"memberName")
      			portNames = ['WC_defaulthost','WC_adminhost','WC_defaulthost_secure','WC_adminhost_secure','BOOTSTRAP_ADDRESS','SOAP_CONNECTOR_ADDRESS','SAS_SSL_SERVERAUTH_LISTENER_ADDRESS','CSIV2_SSL_SERVERAUTH_LISTENER_ADDRESS','CSIV2_SSL_MUTUALAUTH_LISTENER_ADDRESS','DCS_UNICAST_ADDRESS','SIB_ENDPOINT_ADDRESS','SIB_ENDPOINT_SECURE_ADDRESS','SIP_DEFAULTHOST','SIP_DEFAULTHOST_SECURE','SIB_MQ_ENDPOINT_ADDRESS','ORB_LISTENER_ADDRESS','SIB_MQ_ENDPOINT_SECURE_ADDRESS']


			host = dict[nodeName]
			print "Cluster member is "+memberName+" and hostname is "+host
			for portName in portNames:
				print "Setting "+portName+" to "+str(sPort)
				#AdminTask.modifyServerPort(memberName, '[-nodeName '+nodeName+' -endPointName '+portName+' -host '+host+' -port '+str(sPort)+' -modifyShared true ]')
				AdminTask.modifyServerPort(memberName, '[-nodeName '+nodeName+' -endPointName '+portName+' -host * -port '+str(sPort)+' -modifyShared true ]')
				sPort=sPort+1
			print ""

  	except:
    		print "ERROR - problem settign ports for "+cName
    		print sys.exc_info()[0]
    		print sys.exc_info()[1]

  	else:
    		AdminConfig.save()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main program
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

envName=sys.argv[0]
basePort=int(sys.argv[1])
clusterLabel=sys.argv[2]
startPort=basePort+50

cell = AdminConfig.list('Cell')
cellName = AdminConfig.showAttribute(cell, 'name')

print "Setting "+clusterLabel+" ports starting at port "+str(startPort)
modPorts(clusterLabel, startPort)

