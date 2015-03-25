#
# The OCD version I really didn't like the way the second argument was just a long string, 
# so I worked out that you can also do it like this...  (not really sure if it's any simpler though) 
# 
import sys

war = sys.argv[0]
cluster = sys.argv[1]

AdminApp.install(war, ['-MapWebModToVH', [['.*',  '.*',  'default_host']], '-MapModulesToServers', [['.*',  '.*',  'WebSphere:cluster='+cluster ]]])

AdminConfig.save()
