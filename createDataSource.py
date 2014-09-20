# createDataSource.py
# Author: Bob Clarke
# Date: 28/08/2014

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set up
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import sys

cellName=sys.argv[0]
providerName=sys.argv[1]
providerType=sys.argv[2]
userName=sys.argv[3]
password=sys.argv[4]
dsName=sys.argv[5]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Define subs
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def createProvider():
	print "Creating JDBC Provider"
	AdminTask.createJDBCProvider('[-scope Cell='+cellName+' -databaseType Oracle -providerType "Oracle JDBC Driver" -implementationType "XA data source" -name "Oracle JDBC Driver (XA)" -description "Oracle JDBC Driver (XA)" -classpath [/home/vmfest/was/drivers/oracle/ojdbc14.jar] -nativePath "" ]') 

def createAuthAlias():
	print "Creating Auth Alias"
	security = AdminConfig.getid('/Security:/')
	alias = ['alias', dsName+'_alias']
	userid = ['userId', userName]
	pw = ['password', password]
	jaasAttrs = [alias, userid, pw]
	aliasId = AdminConfig.create('JAASAuthData', security, jaasAttrs)

def createDataSource():
	print "Creating DataSource"

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main program
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
createProvider()
createAuthAlias()
createDataSource()



# AdminConfig.create('ResourceEnvironmentProvider', AdminConfig.getid('/Cell:salsaCell1/'), '[[classpath ""] [name "bobRP"] [isolatedClassLoader "false"] [nativepath ""] [description ""]]') 

# jdbc:oracle:thin:@p19803dev060-dat.test.lloydstsb.co.uk:1522:GXYAPP1D
