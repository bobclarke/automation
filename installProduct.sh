#!/bin/bash

message()
{
	echo "<BUILD> $1"
}

props=config.props
[ ! -s "$props" ] && echo "$0 : cannot find properties file $props" && exit 1
. ./"$props" > /dev/null 2>&1

while [ $# -ne 0 ] ;  do
  pkgName=$(echo "${1:-''}" | tr '[A-Z]' '[a-z]')
  case "$pkgName" in

    enablesec)
	message "Enabling application security"
	$wasInstallDir/profiles/${dmgrProf}/bin/wsadmin.sh -lang jython -user $wasUser -password $wasPass -f enableSec.py
        ;;

    download)
	./download.sh
        ;;

    download6)
	./download_v6.sh
        ;;

    im) responseFile=$(pwd)/im.resp
	message "Installing Installation Manager"
        $imSrcDir/userinstc -acceptLicense -input $responseFile -silent 
        ;;

    was6) responseFile=$(pwd)/was6.resp
        message "Installing WAS6 binaries"
        #$wasSrcDir/install -options $responseFile -silent
	[ ! -s "$wasInstallDir" ] &&  mkdir $wasInstallDir
	tar -xpf ${localRepo}/${was6Image} --keep-old-files --directory $wasInstallDir
        ;;

    enablejdk7)
	message "Enabling JDK 7"
	./enableJava7.sh
        ;;

    configsalsalibs)
	message "Configuring shared lib for RPC"
	$wasInstallDir/profiles/${dmgrProf}/bin/wsadmin.sh -lang jython -user $wasUser -password $wasPass -f configSalsaLibs.py $clusterName $rpcSharedLib $cellName $rpcWar $nodeProf $rpcName $rpcSharedLibCp $rpcName
        ;;

    deployivt)
	message "Deploying IVT"
	$wasInstallDir/profiles/${dmgrProf}/bin/wsadmin.sh -lang jython -user $wasUser -password $wasPass -f deployEar.py $clusterName $localRepo ${profilePath}/${dmgrProfile}/installableApps/ivt.ear "ivtApp" $cellName
        ;;

    deploysnoop)
	message "Deploying Snoop"
	$wasInstallDir/profiles/${dmgrProf}/bin/wsadmin.sh -lang jython -user $wasUser -password $wasPass -f deploySnoop.py $clusterName $wasInstallDir
        ;;

    deploysnoop6)
	message "Deploying Snoop"
	$wasInstallDir/profiles/${dmgrProf}/bin/wsadmin.sh -lang jython -user $wasUser -password $wasPass -f deploySnoop_v6.py $clusterName $wasInstallDir
        ;;

    deploysalsa)
	message "Deploying RPC"
	$wasInstallDir/profiles/${dmgrProf}/bin/wsadmin.sh -lang jython -user $wasUser -password $wasPass -f deployWar.py $clusterName $localRepo $rpcWar $rpcCr $rpcName $cellName
	#message "Deploying RPC-RM"
	#$wasInstallDir/profiles/${dmgrProf}/bin/wsadmin.sh -lang jython -user $wasUser -password $wasPass -f deployWar.py $clusterName $localRepo $rpcRmWar $rpcRmCr $rpcRmName $cellName
        ;;

    was) responseFile=$(pwd)/was.resp
	message "Installing WAS"
	$installDir/im/eclipse/IBMIM -acceptLicense -input $responseFile -silent -nosplash
        ;;

    commondb)
	message "Creating CommonDB"
	${profilePath}/${dmgrName}/dbscripts/CommonDB/Oracle/${commonSchema}/configCommonDB.sh
        ;;

    bpcdb)
	message "Creating Process Choreographer DB"
	. $sqlPlusEnv
	echo sqlplus ${bpcUser}/${bpcSchemaPass}@${dbName} @${profilePath}/${dmgrName}/dbscripts/ProcessChoreographer/Oracle/XE/XEBE00/createSchema.sql
        ;;

    waspatch) responseFile=$(pwd)/waspatch.resp
	message "Installing 8.5.5 fixpack for WAS"
	$installDir/im/eclipse/IBMIM -acceptLicense -input $responseFile -silent -nosplash
        ;;

    dmgr) responseFile=$(pwd)/dmgr.resp
	message "Creating Deployment Manager profile"
        $wasInstallDir/bin/manageprofiles.sh -response $responseFile
        ;;

    dmgr6) responseFile=$(pwd)/dmgr_v6.resp
	message "Creating Deployment Manager profile"
        $wasInstallDir/bin/manageprofiles.sh -response $responseFile
        ;;

    was6) responseFile=$(pwd)/was6.resp
	message "Installing WAS6 binaries"
        $localRepo/install -options $responseFile -silent
        ;;

    node6) responseFile=$(pwd)/node_v6.resp
	message "Creating Node profile"
        $wasInstallDir/bin/manageprofiles.sh -response $responseFile
        ;;

    startdmgr)
	message "Starting Deployment Manager"
        $wasInstallDir/profiles/${dmgrProf}/bin/startManager.sh
        ;;

    stopdmgr)
	message "Stopping Deployment Manager"
        $wasInstallDir/profiles/${dmgrProf}/bin/stopManager.sh -user $wasUser -password $wasPass
        ;;

    startnode)
	message "Starting Nodeagent"
        $wasInstallDir/profiles/${nodeProf}/bin/startNode.sh
        ;;

    stopnode)
	message "Stopping Nodeagent"
        $wasInstallDir/profiles/${nodeProf}/bin/stopNode.sh -user $wasUser -password $wasPass
        ;;

    stopclusters) 
	message "Stopping Clusters"
	$wasInstallDir/profiles/${dmgrProf}/bin/wsadmin.sh -lang jython -user $wasUser -password $wasPass -f stopClusters.py
        ;;

    startclusters) 
	message "Starting Clusters"
	$wasInstallDir/profiles/${dmgrProf}/bin/wsadmin.sh -lang jython -user $wasUser -password $wasPass -f startClusters.py
        ;;

    depenv) 
	message "Building Deployment Environment for $envName"
	$wasInstallDir/profiles/${dmgrProf}/bin/wsadmin.sh -lang jython -user $wasUser -password $wasPass -f genDepEnv.py $envName
        ;;

    confrpc) 
	message "Configuring RPC backend services"
	$wasInstallDir/profiles/${dmgrProf}/bin/wsadmin.sh -lang jython -user $wasUser -password $wasPass -f configRpc.py $salsaDbUser $salsaDbPass $salsaDbHost $salsaDbPort $salsaDbName $slrProtocol $slrHost $slrPort $slrUri $ciaProtocol $ciaHost $ciaPort $ciaUri $salsaDbJndi
        ;;

    stopihs)
	message "Stopping IHS"
	$ihsInstallDir/bin/apachectl stop
        ;;

    startihs)
	message "Starting IHS"
	$ihsInstallDir/bin/apachectl start
        ;;

    basenode) responseFile=$(pwd)/basenode.resp
	message "Creating Base profile"
        $wasInstallDir/bin/manageprofiles.sh -response $responseFile
        ;;

    node) responseFile=$(pwd)/node.resp
	message "Creating Node profile"
        $wasInstallDir/bin/manageprofiles.sh -response $responseFile
        ;;

    addnode) 
	echo "Federating Node"
	$(pwd)/addNode.sh
        ;;

    addnode6) 
	echo "Federating Node (V6)"
	$(pwd)/addNode_v6.sh
        ;;

    vhost) 
	message "Configuring Virtual Host aliases"
	$wasInstallDir/profiles/${dmgrProf}/bin/wsadmin.sh -lang jython -user $wasUser -password $wasPass -f vhost.py
        ;;

    cluster) 
	message "Creating Cluster"
	$wasInstallDir/profiles/${dmgrProf}/bin/wsadmin.sh -lang jython -user $wasUser -password $wasPass -f createCluster.py $clusterName $clusterBasePort $nodeName
        ;;

    cluster6) 
	message "Creating Cluster (V6)"
	$wasInstallDir/profiles/${dmgrProf}/bin/wsadmin.sh -lang jython -user $wasUser -password $wasPass -f createCluster_v6.py $clusterName $clusterBasePort $nodeName
        ;;

    setports) 
	$wasInstallDir/profiles/${dmgrProf}/bin/wsadmin.sh -lang jython -user $wasUser -password $wasPass -f setPorts.py $envName $clusterBasePort $clusterName 
        ;;

    setwpsports) 
	$wasInstallDir/profiles/${dmgrProf}/bin/wsadmin.sh -lang jython -user $wasUser -password $wasPass -f setPorts.py $envName $appBasePort $AppTargetClusterName
	$wasInstallDir/profiles/${dmgrProf}/bin/wsadmin.sh -lang jython -user $wasUser -password $wasPass -f setPorts.py $envName $messBasePort $MessagingClusterName
	$wasInstallDir/profiles/${dmgrProf}/bin/wsadmin.sh -lang jython -user $wasUser -password $wasPass -f setPorts.py $envName $suppBasePort $SupportClusterName
        ;;

    ihs) responseFile=$(pwd)/ihs.resp
	message "Installing IHS"
	$installDir/im/eclipse/IBMIM -acceptLicense -input $responseFile -silent -nosplash
        ;;

    plg) responseFile=$(pwd)/plg.resp
	message "Installing IHS Plugin"
	$installDir/im/eclipse/IBMIM -acceptLicense -input $responseFile -silent -nosplash

	PLG_CONF=${wasInstallDir}/profiles/${dmgrName}/config/cells/plugin-cfg.xml
	HTTPD_CONF=${ihsInstallDir}/conf/httpd.conf
	PLG_MOD=${plgInstallDir}/bin/64bits/mod_was_ap22_http.so

	message "Updating $HTTPD_CONF"
	echo ""
	echo "### WebSphere plugin" >> $HTTPD_CONF

	echo "LoadModule was_ap22_module $PLG_MOD" >> $HTTPD_CONF
	echo "WebSpherePluginConfig ${PLG_CONF}" >> $HTTPD_CONF
	;;

    genplg)
	message "Generating plugin"
	${wasInstallDir}/bin/GenPluginCfg.sh
	;;


    uninstall) 
	message "Uninstalling..."
	dirList="$installDir/.ibm $installDir/var/ibm $installDir/etc/.ibm $installDir/im $installDir/eclipsecache $wasInstallDir $ihsInstallDir $plgInstallDir $installDir/.config/menus/applications-merged/WebSphere.menu $installDir/waslogs $installDir/webserviceslogs $installDir/wbilogs $installDir/responsefile.* $installDir/vpd.properties"
	for dir in $dirList
	do
		message "Removing $dir if it exists"
		if [ -d $dir ]; then rm -r $dir ; fi
	done
	message "Uninstall complete."
        ;;

    message)
	message "Build complete" 
	message "SOAP port is $dmgrSoapPort"
	message "Admin console is https://${hostName}:${dmgrAdminSecurePort}/admin (assuming you can resolve $hostName)"
	message "Web Container port is $clusterBasePort"
	message "You can test the server by running Snoop at http://${hostName}:${clusterBasePort}/snoop"
        ;;
    *) echo "${0##*/}: unknown product $pkgName" && exit ;;
  esac
  shift
done

echo "" 
