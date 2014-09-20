#!/bin/bash

# enableJava7.sh
# Author: Bob Clarke
# Date: 10/06/2014

#---------------------------------------------------------------------
# Setup 
#---------------------------------------------------------------------
props=config.props
[ ! -s "$props" ] && echo "$0 : cannot find properties file $props" && exit 1
. ./"$props" > /dev/null 2>&1

#---------------------------------------------------------------------
# Functions  
#---------------------------------------------------------------------

message()
{
        echo "<BUILD> $1"
}

config()
{
	message "Backing up JDK6 config"
	cp -rp ${wasInstallDir}/properties/sdk $wasInstallDir/properties/sdk.backup
	cp -rp ${wasInstallDir}/bin/sdk $wasInstallDir/bin/sdk.backup
	cd $wasInstallDir

	message "Unpacking JDK7"
	tar -xpf ${localRepo}/java_1.7_64.tar

	message "Unpacking WAS config for JDK7"
	tar -xpf ${localRepo}/java_1.7_64_config.tar
	mv node-metadata.properties ${wasInstallDir}/profiles/${dmgrProf}/config/cells/${cellName}/nodes/${nodeName}/node-metadata.properties
}

sync()
{
	# Get the Deployment Manager's SOAP port directly from serverindex.xml
	# Most reliable method I could come up with to derive SOAP port without using wsadmin

	serverIndex=${profilePath}/${dmgrProf}/config/cells/${cellName}/nodes/${dmgrName}Node/serverindex.xml
	derivedSoapPort=`awk '/SOAP_CONNECTOR_ADDRESS/,/port/' $serverIndex | grep host | grep port | sed s/.*port=\"// | sed s:\"/\>::`

	message "Deriving DMGR SOAP port"
	message "serverindex file is $serverIndex"
	message "DMGR SOAP port is $derivedSoapPort"

	message "Stopping node"
	${wasInstallDir}/profiles/$nodeProf/bin/stopNode.sh -user ${wasUser} -password ${wasPass}

	message "Syncronising node"
	${wasInstallDir}/profiles/$nodeProf/bin/syncNode.sh $dmgrHost $derivedSoapPort -username ${wasUser} -password ${wasPass}

	message "Starting node"
	${wasInstallDir}/profiles/$nodeProf/bin/startNode.sh
}

enableDmgr()
{
	message "Enabling JDK7 on $dmgrName"
	${wasInstallDir}/profiles/${dmgrProf}/bin/managesdk.sh -enableProfile -profileName ${dmgrProf} -enableServers -sdkname 1.7_64
}

enableNode()
{
	message "Enabling JDK7 on $nodeName"
	${wasInstallDir}/profiles/${nodeProf}/bin/managesdk.sh -enableProfile -profileName ${nodeProf} -enableServers -sdkname 1.7_64 -user $wasUser -password $wasPass
}


#---------------------------------------------------------------------
# Main  
#---------------------------------------------------------------------
config
enableDmgr
enableNode
sync
message "Running ${wasInstallDir}/bin/managesdk.sh -listEnabledProfileAll"
${wasInstallDir}/bin/managesdk.sh -listEnabledProfileAll
