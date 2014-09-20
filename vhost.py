# vhost.py
# Author: Bob Clarke 
# Date: 23/06/2014
#


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set up
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import sys
cell=AdminConfig.list('Cell')
cellName=AdminConfig.showAttribute(cell, 'name')
vhostId=AdminConfig.getid('/Cell:' + cellName + '/VirtualHost:default_host/')
print vhostId

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Define subs
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def removeExistingAliases():
	for alias in AdminConfig.list('HostAlias', vhostId).splitlines():
		AdminConfig.remove(alias)
	
def addAlias(host, port):
	AdminConfig.create('HostAlias', vhostId, '[[hostname "' + host + '"] [port "' + port + '"]]')

def listAliases ():
	for alias in AdminConfig.list('HostAlias', vhostId).splitlines():
		print AdminConfig.show(alias)
		print
	
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main program
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
removeExistingAliases()
addAlias('*','*')
AdminConfig.save()

