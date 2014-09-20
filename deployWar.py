# deployWar.py
# Author: Bob Clarke
# Date: 03/06/2014

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set up
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import sys
cluster=sys.argv[0]
repo=sys.argv[1]
war=sys.argv[2]
cr=sys.argv[3]
name=sys.argv[4]
cell=sys.argv[5]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Subs 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def deploy():
	print 'Installing '+war+' as '+name+' with a context root of '+cr

	AdminApp.install( repo+ '/' +war, '[ -appname '+name+' -nopreCompileJSPs -distributeApp -nouseMetaDataFromBinary -nodeployejb -createMBeansForResources -noreloadEnabled -nodeployws -validateinstall warn -noprocessEmbeddedConfig -filepermission .*\.dll=755#.*\.so=755#.*\.a=755#.*\.sl=755 -noallowDispatchRemoteInclude -noallowServiceRemoteInclude -asyncRequestDispatchType DISABLED -nouseAutoLink -noenableClientModule -clientMode isolated -novalidateSchema -contextroot /' + cr + ' -MapModulesToServers [[ '+name+' '+war+',WEB-INF/web.xml WebSphere:cell='+cell+',cluster='+cluster+' ]] -MapWebModToVH [[ '+name+' '+war+',WEB-INF/web.xml default_host ]] -CtxRootForWebMod [[ '+name+' '+war+',WEB-INF/web.xml /'+cr+' ]]]' ) 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

deploy()

AdminConfig.save()
