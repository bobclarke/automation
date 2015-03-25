#
# It's worth noting that only -MapWebModToVH and -MapModulesToServer are required, 
# therefore a if you're in a hurry you can use a shorter version
#
import sys

war = sys.argv[0]
cluster = sys.argv[1]

AdminApp.install(war, '[-MapWebModToVH [[ .* .* default_host ]] -MapModulesToServers [[ .* .* WebSphere:cluster='+cluster+']]]')

AdminConfig.save()
