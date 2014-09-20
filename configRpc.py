# configSalsa.py
# Author: Bob Clarke
# Date: 07/05/2014


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set up
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import sys
dbUser=sys.argv[0]
dbPass=sys.argv[1]
dbHost=sys.argv[2]
dbPort=sys.argv[3]
dbName=sys.argv[4]
dbJndi=sys.argv[13]

slrProtocol=sys.argv[5]
slrHost=sys.argv[6]
slrPort=sys.argv[7]
slrUri=sys.argv[8]

ciaProtocol=sys.argv[9]
ciaHost=sys.argv[10]
ciaPort=sys.argv[11]
ciaUri=sys.argv[12]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Subs
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def createAuthAlias(dbUser, password, alias):
	alias = ['alias', alias]
	userid = ['userId', user]
	password = ['password', password]
	attrs = [alias, user, password]
	security = AdminConfig.list('Security')
	AdminConfig.create('JAASAuthData', security, attrs)

def removeDs(dsname):
        for ds in AdminConfig.list('DataSource').splitlines():
                jndiName = AdminConfig.showAttribute(ds, 'jndiName')
                if( jndiName.find(dsname) != -1):
                        print "have found "+ds +" removing"
                        AdminConfig.remove(ds)

def removeAuthAlias(aaname):
        for aa in AdminConfig.list('JAASAuthData').splitlines():
                alias = AdminConfig.showAttribute(aa, 'alias')
                if( alias.find(aaname) != -1):
                        print "have found "+aa +" removing"
                        AdminConfig.remove(aa)


def createdb():
	print '\n'
	myPrint('Creating  datasource')

	for ds in AdminConfig.list("DataSource").splitlines():
		jndiName = AdminConfig.showAttribute(ds, 'jndiName')
		l_jndiName = jndiName.lower()
		if(l_jndiName.find('ref_data') != -1):

			# Auth alias
			authAlias = AdminConfig.showAttribute(ds, 'authDataAlias')
			for ad in AdminConfig.list("JAASAuthData").splitlines():
				alias = AdminConfig.showAttribute(ad, 'alias')
				l_alias = alias.lower()
				if (l_alias.find(authAlias.lower()) != -1):
					myPrint ('\tUpdating authentication data for '+alias) 
					AdminConfig.modify(ad, [['userId', dbUser]])
					AdminConfig.modify(ad, [['password', dbPass]])

			# URL
			ps = AdminConfig.showAttribute(ds, 'propertySet')
			for prop in AdminConfig.show(ps).split():
				if(prop.find('URL') != -1):
					url = 'jdbc:oracle:thin:@' + dbHost + ':' + dbPort + ':' + dbName
					myPrint ('\tUpdating JDBC connection string for '+jndiName+' to '+url)
					AdminConfig.modify(prop, [['value', 'jdbc:oracle:thin:@' + dbHost + ':' + dbPort + ':' + dbName ]])


def myPrint(s):
	print '<BUILD> '+s


def wsc(app, protocol, host, tcpPort, uri):
        print('\n<BUILD> Configuring '+app+' web service endpoints')
	moduleConf = AdminApp.view(app + 'App#' + app + 'EJB.jar+META-INF/ejb-jar.xml', '[-WebServicesClientBindPortInfo]')

	# split into services
	moduleConfArray = moduleConf.split(app+'EJB.jar')
	
	# Delete the first element of the array (it's empty)
	moduleConfArray.pop(0)

	for service in moduleConfArray:
		
		# Now search for the relevant lines in each service
		for line in service.splitlines():
			if(line.find('Web service:') != -1):
				ws = line.split(':')[1].strip()
				myPrint('\tWS is: '+ws)
			elif(line.find('port:') != -1):
				wsport = line.split(':')[1].strip()
				myPrint('\tWS PORT is: '+wsport)

		myPrint( '\tPROTOCOL is :'+protocol)
		myPrint( '\tPORT is :'+tcpPort)
		myPrint( '\tHOST is :'+host)
		print

		AdminApp.edit(app+'App', '[-WebServicesClientBindPortInfo [['+ app + 'EJB.jar Module '+ ws +' ' + wsport +' "" "" "" "" '+protocol+'://'+ host +':'+ tcpPort + uri +' ""]]]')
			
def db():
	print '\n'
	myPrint('Configuring database')

	# Modify data source 
	for ds in AdminConfig.list("DataSource").splitlines():
		jndiName = AdminConfig.showAttribute(ds, 'jndiName')
		l_jndiName = jndiName.lower()
		if(l_jndiName.find('ref_data') != -1):

			# Auth alias
			authAlias = AdminConfig.showAttribute(ds, 'authDataAlias')
			for ad in AdminConfig.list("JAASAuthData").splitlines():
				alias = AdminConfig.showAttribute(ad, 'alias')
				l_alias = alias.lower()
				if (l_alias.find(authAlias.lower()) != -1):
					myPrint ('\tUpdating authentication data for '+alias) 
					AdminConfig.modify(ad, [['userId', dbUser]])
					AdminConfig.modify(ad, [['password', dbPass]])

			# URL
			ps = AdminConfig.showAttribute(ds, 'propertySet')
			for prop in AdminConfig.show(ps).split():
				if(prop.find('URL') != -1):
					url = 'jdbc:oracle:thin:@' + dbHost + ':' + dbPort + ':' + dbName
					myPrint ('\tUpdating JDBC connection string for '+jndiName+' to '+url)
					AdminConfig.modify(prop, [['value', 'jdbc:oracle:thin:@' + dbHost + ':' + dbPort + ':' + dbName ]])

			

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main program
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#wsc('PM_RetrievePromotionalCommunications', slrProtocol, slrHost, slrPort, slrUri)
#wsc('MM_OUT_CIA', ciaProtocol, ciaHost, ciaPort, ciaUri)
#db()

removeDs('ref_data')
removeAuthAlias('ref_data')

#AdminConfig.save()

# execfile('/opt/ibm/inst/configRpc.py')
# sys.argv = ['SALSA1_SCHEMA','h0liday','p19803dev060-dat.test.lloydstsb.co.uk,','1522','GXYAPP1T.test.lloydstsb.co.uk','http','10.245.211.251','22518','/PM_LeadServiceWeb/sca/ID_LeadServiceExport1','http','zdev3.service.test.group','60928','/CICS/F139/VU0015CE']
