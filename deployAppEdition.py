# deployAppEdition.py 
# Author: Bob Clarke
# Date: 14/07/2014

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set up
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import sys
cluster=sys.argv[0]
wasInstallDir=sys.argv[1]
version=sys.argv[2]

cellId=AdminConfig.list('Cell')
cell=AdminConfig.showAttribute(cellId, 'name')
rp = AdminControl.queryNames('name=repository,process=nodeagent,*')
cs = AdminControl.queryNames('name=cellSync,*')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Subs
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def deploy():
        print 'Installing Snoop version '+version+' from '+wasInstallDir

        AdminApp.install(wasInstallDir+'/installableApps/DefaultApplication.ear', '[ -nopreCompileJSPs -distributeApp -nouseMetaDataFromBinary -nodeployejb -appname DefaultApplication_V'+version+' -createMBeansForResources -noreloadEnabled -nodeployws -validateinstall warn -noprocessEmbeddedConfig -filepermission .*\.dll=755#.*\.so=755#.*\.a=755#.*\.sl=755 -noallowDispatchRemoteInclude -noallowServiceRemoteInclude -MapModulesToServers [[ "Increment Enterprise Java Bean" Increment.jar,META-INF/ejb-jar.xml WebSphere:cell='+cell+',cluster='+cluster+' ][ "Default Web Application" DefaultWebApplication.war,WEB-INF/web.xml WebSphere:cell='+cell+',cluster='+cluster+' ]]]' )

def deploy_verification ():
        print 'Installing Snoop version '+version+' from '+wasInstallDir+' with CTX of /snoop_'+version

        AdminApp.install(wasInstallDir+'/installableApps/DefaultApplication.ear', '[ -nopreCompileJSPs -distributeApp -nouseMetaDataFromBinary -nodeployejb -appname DefaultApplication_V'+version+' -createMBeansForResources -noreloadEnabled -nodeployws -validateinstall warn -noprocessEmbeddedConfig -filepermission .*\.dll=755#.*\.so=755#.*\.a=755#.*\.sl=755 -noallowDispatchRemoteInclude -noallowServiceRemoteInclude -MapModulesToServers [[ "Increment Enterprise Java Bean" Increment.jar,META-INF/ejb-jar.xml WebSphere:cell='+cell+',cluster='+cluster+' ][ "Default Web Application" DefaultWebApplication.war,WEB-INF/web.xml WebSphere:cell='+cell+',cluster='+cluster+' ]] -CtxRootForWebMod [[ "Default Web Application"  DefaultWebApplication.war,WEB-INF/web.xml /snoop_'+version+' ]]]' )


def sync():
        print 'Syncronising Cell'
	AdminControl.invoke(rp, 'refreshRepositoryEpoch') 
	AdminControl.invoke(cs, 'syncNode', '[autoWasNode1]', '[java.lang.String]') 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

deploy()
#deploy_verification()
AdminConfig.save()
sync()

# execfile('/opt/ibm/inst/deployAppEdition.py')
