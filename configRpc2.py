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
                alias = AdminConfig.showAttribute(aa, 'alias').lower()
		print alias
                if( alias.find(aaname.lower()) != -1):
                        print "have found "+aa +" removing"
                        AdminConfig.remove(aa)

def createDs(name, jp, host, port, sid, helper, aa):
	AdminTask.createDatasource('', '[-name '+ name +' -jndiName jdbc/'+name+' -dataStoreHelperClassName '+helper+' -componentManagedAuthenticationAlias '+aa+' -xaRecoveryAuthAlias '+aa+' -configureResourceProperties [[URL java.lang.String jdbc:postgree:thin:@10.245.211.203:1522/gxymny1d.test.lloydstsb.co.uk]]]') 









        myPrint('Creating  datasource')
	url = 'jdbc:oracle:thin:@' + host + ':' + port + ':' + name
	print ('\tUpdating JDBC connection string for '+jndiName+' to '+url)
	AdminConfig.modify(prop, [['value', 'jdbc:oracle:thin:@' + dbHost + ':' + dbPort + ':' + dbName ]])

def createJdbcProvider(name, class):
	name = ['name', name]
	implcn = ['implementationClassName', class]
        attrs = [name, implcn]
	
def removeJdbcProvider(name):
	print name
	


	

#  execfile('/opt/ibm/git/salsa-poc/infrastructure/websphere-automation/foo.py')
removeDs('ref_data')
removeAuthAlias('REF_DATA')
#AdminConfig.save()
