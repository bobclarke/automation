# deployAppEdition.py 
# Author: Bob Clarke
# Date: 14/07/2014

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set up
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import sys
version=sys.argv[0]

cellId=AdminConfig.list('Cell')
cell=AdminConfig.showAttribute(cellId, 'name')
rp = AdminControl.queryNames('name=repository,process=nodeagent,*')
cs = AdminControl.queryNames('name=cellSync,*')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Subs
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def undeploy():

	try:
        	AdminApp.uninstall('DefaultApplication_V'+version)

	except :
		#print "Slight error, nothing to worry about"
		AdminConfig.save()

def sync():
        print 'Syncronising Cell'
        AdminControl.invoke(rp, 'refreshRepositoryEpoch')
        AdminControl.invoke(cs, 'syncNode', '[autoWasNode1]', '[java.lang.String]')


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

undeploy()
sync()
