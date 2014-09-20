#/bin/sh -x

# addNode.sh
# Author: Bob Clarke
# Date: 10/07/2014
#
# Had to externalise this as I had a nightmare assiging the SOAP port to a variable in the Makefile

props=config.props
[ ! -s "$props" ] && echo "$0 : cannot find properties file $props" && exit 1
. ./"$props" > /dev/null 2>&1

# Most reliable method I could come up with to derive SOAP port without using wsadmin 
serverIndex=${profilePath}/${dmgrProf}/config/cells/${cellName}/nodes/${dmgrName}Node/serverindex.xml
derivedSoapPort=`awk '/SOAP_CONNECTOR_ADDRESS/,/port/' $serverIndex | grep host | grep port | sed s/.*port=\"// | sed s:\"/\>::`

echo "DMGR port is $derivedSoapPort"

cmd=${profilePath}/${nodeProf}/bin/addNode.sh
$cmd $dmgrHost $derivedSoapPort -startingport $nodeBasePort -user $wasUser -password $wasPass
