# deploySnoop_v6.py - I'm sure there's a better way but for now I need a sepearte 
# version of this for WAS 6 because the EJB module name is different between versions
# Author: Bob Clarke
# Date: 24/06/2014

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set up
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import sys
cluster=sys.argv[0]
wasInstallDir=sys.argv[1]
cellId=AdminConfig.list('Cell')
cell=AdminConfig.showAttribute(cellId, 'name')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Subs 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def deploy():
	print 'Installing Snoop from '+wasInstallDir


	AdminApp.install(wasInstallDir+'/installableApps/DefaultApplication.ear', '[ -nopreCompileJSPs -distributeApp -nouseMetaDataFromBinary -nodeployejb -appname DefaultApplication.ear -createMBeansForResources -noreloadEnabled -nodeployws -validateinstall warn -noprocessEmbeddedConfig -filepermission .*\.dll=755#.*\.so=755#.*\.a=755#.*\.sl=755 -noallowDispatchRemoteInclude -noallowServiceRemoteInclude -MapModulesToServers [[ "Increment Enterprise Java Bean" Increment.jar,META-INF/ejb-jar.xml WebSphere:cell='+cell+',cluster='+cluster+' ][ "Default Web Application" DefaultWebApplication.war,WEB-INF/web.xml WebSphere:cell='+cell+',cluster='+cluster+' ]]]' ) 


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

deploy()
AdminConfig.save()
