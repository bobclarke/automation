import sys

war = sys.argv[0]
name = sys.argv[1]
cluster = sys.argv[2]
cr = sys.argv[3]
cellId = AdminConfig.list('Cell')
cell = AdminConfig.showAttribute(cellId, 'name')

 AdminApp.install(war, '[ -appname '+name+' -contextroot '+cr+' -MapModulesToServers [[ .* .* WebSphere:cell='+cell+',cluster='+cluster+' ]] -MapWebModToVH [[ .* .* default_host ]] -CtxRootForWebMod [[ .* .* '+cr+' ]]]' )

AdminConfig.save()
