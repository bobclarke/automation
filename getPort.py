# getPort.py
# Author: Bob Clarke 
# Date: 10/07/2014
#
# Return port number given a named endpoint


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set up
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import sys
nep=sys.argv[0]
#nep="SOAP_CONNECTOR_ADDRESS"


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main program
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
dmgr = AdminConfig.getid('/Server:dmgr/')
soapConnector = AdminConfig.list('SOAPConnector', dmgr)
soapConnectorAddress = AdminConfig.showAttribute(soapConnector, nep)
port = AdminConfig.showAttribute(soapConnectorAddress, 'port')
print port
