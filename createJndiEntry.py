# createJndiEntry.py
# Author: Bob Clarke
# Date: 28/08/2014

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Define subs
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def repExists(repName):
	print 'Checking if Resource Env Provider '+repName+' exists' 
	rep = AdminConfig.getid('/ResourceEnvironmentProvider:'+repName+'/')
	return rep

def createRep(repName):
	print 'Creating Resource Env Provider with name '+repName
	rep = AdminConfig.create('ResourceEnvironmentProvider', cellId, [['name',repName]] )
	# Not sure why I need this "Referencable", seems to be a requirement
	AdminConfig.create('Referenceable', rep, [['factoryClassname', 'fClass1'],['classname', 'Class1']])
	return rep

def reeExists(key):
	print 'Checking if jndi entry of salsa/'+key+' exists'
	ree = AdminConfig.getid('/ResourceEnvEntry:'+key+'/')
	return ree

def createJndiRef(rep,key):
	print 'Creating JNDI entry salsa/'+key
	ree = AdminConfig.create('ResourceEnvEntry', rep, [['name', key], ['jndiName', 'salsa/'+key]]) 
	return ree

def createPropSet(ree,key):
	print 'Creating an empty property set'
	propSet = AdminConfig.create('J2EEResourcePropertySet',ree, [])
	return propSet

def createProp(propSet,key):
	print 'Creating property, key='+key+' : value='+val
	AdminConfig.create('J2EEResourceProperty', propSet, [['name', key], ['type', 'java.lang.String'], ['value', val], ['required', 'false']]) 

	
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Setup
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

repName = sys.argv[0]
key = sys.argv[1]
val = sys.argv[2]
cellId = AdminConfig.getid('/Cell:/')
rep=""
ree=""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main program
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
existingRep=repExists(repName)
if existingRep:
	print repName+' exists'
	print 'Setting rep to '+str(existingRep)
	rep=existingRep
else:
	rep=createRep(repName)
	
existingRee=reeExists(key)

if existingRee:
	print 'salsa/'+key+' exists'
	print 'Setting ree to '+str(existingRee)
	ree=existingRee
else:
	ree=createJndiRef(rep,key)

propSet=createPropSet(ree,key)
createProp(propSet,key)
AdminConfig.save()

