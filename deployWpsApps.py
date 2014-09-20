# deployWpsApps.py
# Author: Bob Clarke
# Date: 22/08/2014

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set up
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import sys
earList=sys.argv[0]
srcDir=sys.argv[1]
cluster=sys.argv[2]
cellId=AdminConfig.list('Cell')
cell=AdminConfig.showAttribute(cellId, 'name')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Subs 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def deploy(earList):

	for ear in earList.split():
		mm ='WebSphere:cell='+cell+',cluster='+cluster
		print srcDir+'/'+ear
		print mm
		print 

		#AdminApp.install(srcDir+'/'+ear, [ '-MapModulesToServers' [['.*','.*', m]['.*','.*', m]] ]) 
		#AdminConfig.save()



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

deploy(earList)
