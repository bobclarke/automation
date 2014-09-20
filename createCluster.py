# createCluster.py
# Author: Bob Clarke 
# Date: 04/03/2014
#
# Currently only supports two members on a single node, needs improving.


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set up
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import sys
clusterName=sys.argv[0]
clusterBasePort=sys.argv[1]
nodeName=sys.argv[2]
member1=clusterName+'Member1'
member2=clusterName+'Member2'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Define subs
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def createCluster(clusterName):
	AdminTask.createCluster('[-clusterConfig [-clusterName '+ clusterName +' -preferLocal true]]') 

	print 'Creating cluster member 1'
def addMembers(clusterName, nodeName, member1, member2):
	AdminTask.createClusterMember('[-clusterName '+clusterName+' -memberConfig [-memberNode '+nodeName+' -memberName '+member1+' -memberWeight 2 -genUniquePorts true -replicatorEntry false] -firstMember [-templateName default -nodeGroup DefaultNodeGroup -coreGroup DefaultCoreGroup -resourcesScope cluster]]') 

	#print 'Creating cluster member 2'
	#AdminTask.createClusterMember('[-clusterName '+clusterName+' -memberConfig [-memberNode '+nodeName+' -memberName '+member2+' -memberWeight 2 -genUniquePorts true -replicatorEntry false]]') 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main program
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
createCluster(clusterName)
addMembers(clusterName, nodeName, member1, member2)
AdminConfig.save()
