: 
# Makefile for auotmated WAS and WPS builds
# Author: Bob Clarke
# Date: May 2014
#
 
#--------------------------------------------------------------------
# Setup 
#--------------------------------------------------------------------
include config.props
include kv.props

WSACMD = 	${wasInstallDir}/profiles/${dmgrProf}/bin/wsadmin.sh \
		-lang jython -user ${wasUser} -password ${wasPass}

RESPONSE = 	depenv.resp dmgr_v6.resp node_v6.resp im.resp was.resp waspatch.resp dmgr.resp \
		node.resp basenode.resp wps6.resp was6.resp dmgr_wps_v6.resp node_wps_v6.resp wasliberty.resp

RESPONSE_DB = 	db_drop_users.resp db_create_users.resp db_scasys_tables.resp db_bpe_tables.resp \
		db_bpeme_tables.resp db_bsp_tables.resp db_common_tables.resp db_create_tablespaces.resp\
		db_scaapp_tables.resp db_ceime_tables.resp db_obs_tables.resp db_drop_tablespaces.resp

UNINST_DIRS = 	${installDir}/.ibm ${installDir}/var/ibm ${installDir}/etc/.ibm \
		${installDir}/eclipsecache ${wasInstallDir} ${ihsInstallDir} ${plgInstallDir} \
		${installDir}/.config/menus/applications-merged/WebSphere.menu ${installDir}/waslogs \
		${installDir}/webserviceslogs ${installDir}/wbilogs  ${installDir}/responsefile.* \
		${installDir}/vpd.properties

MAX_FH = 	8191


#--------------------------------------------------------------------
# Targets
#--------------------------------------------------------------------
all_was6: 	prereqs clean $(RESPONSE) download6 was6 dmgr6 startdmgr enablesec node6 addnode \
		cluster6 setports vhost deploysnoop6 startclusters message

all_wps6: 	prereqs clean response response_db downloadora installora popora downloadwps6 wps6 \
		oradrivers dmgrwps6 startdmgr enablesec nodewps6 addnode depenv vhost \
		startclusters message

all_was8: 	prereqs clean response download im was waspatch dmgr startdmgr enablesec node addnode \
		cluster setports vhost deploysnoop enablejdk7 salsalogging logstash deploysalsa configsalsalibs \
		startclusters message

all_was8_ns: 	prereqs clean response download im was waspatch dmgr startdmgr enablesec node addnode \
		cluster setports vhost deploysnoop enablejdk7 startclusters message

lab: 		clean response im was wasliberty waspatch dmgr startdmgr enablesec node addnode \
		cluster setports vhost deploysnoop enablejdk7 startclusters message


response: ${RESPONSE}

response_db: ${RESPONSE_DB}

startall: startdmgr startnode startclusters

stopall: stopclusters stopnode stopdmgr	

$(RESPONSE):
	@bash ./createResponse.sh $@

$(RESPONSE_DB):
	-@bash ./createResponse.sh $@

getsoapport:
	@echo
	@echo "Getting Deployment Manager SOAP port"
	echo ${soapPort}

prereqs:
	@echo
	@echo "Checking number of file handles available:"
	@fh=`ulimit -n`; if [ $${fh} -gt ${MAX_FH} ] ; then echo "OK - ($$fh file handles available)"; else echo "ERROR: $$fh file handles available, this needs to be at least ${MAX_FH}. Exiting ! "; exit 1; fi

	@# Loopback interface check disabled - ping was never terminating, and we don't have time :( to figure out make-friendly -t param
	@#echo "Checking loopback interface:"
	@#ping localhost

oradrivers:
	-@mkdir -p ${wasInstallDir}/${dbDriverPath}
	ls ${wasInstallDir}/${dbDriverPath} 
	wget -O ${localRepo}/${oracle10gJdbcDriver} --quiet ${oracle10gJdbcRepo}/${oracle10gJdbcDriver}
	@cp ${localRepo}/${oracle10gJdbcDriver} ${wasInstallDir}/${dbDriverPath}

deployedition:
	@echo ""
	@echo "Deploying IBM Snoop application - version ${version}:"
	@${WSACMD} -f deployAppEdition.py ${clusterName} ${wasInstallDir} ${version} | \
		egrep -v '(The following options|The type of process is|Contents of was.policy file)' | \
		egrep -v '(is not found within scope)' | \
		egrep -v '(The resource validation|Duplicate root context|codeBase)'
	@echo ""

undeployedition:
	@echo ""
	@echo "Undeploying IBM Snoop application - version ${version}:"
	@${WSACMD} -f undeployAppEdition.py ${version} | \
		egrep -v '(The following options|The type of process is|cannot be uninstalled)'
	@echo ""

listinstalled:
	@echo ""
	@echo "Listing installed applications:"
	@${WSACMD} -c 'print AdminApp.list()' | grep -v 'The type of process is:'
	@echo "" 

enablesec:
	@echo
	@echo "Enabling application security"
	@${WSACMD} -f enableSec.py

download:
	@echo
	@-mkdir -p ${localRepo}

	@echo "Downloading IM distribution"
	wget -O ${localRepo}/${imDist} --quiet ${imRepo}/${imDist}

	@echo "Unpacking IM"
	unzip -o -d ${localRepo}/im ${localRepo}/${imDist} > /dev/null 2>&1 

	@echo "Downloading WAS 8 distribution"
	wget -O ${localRepo}/${was8Dist} --quiet ${was8Repo}/${was8Dist}
	wget -O ${localRepo}/${was8Patch} --quiet ${was8Repo}/${was8Patch}

	@echo "Unpacking WAS"
	tar -xpf ${localRepo}/${was8Dist} -C ${localRepo}/
	@echo "Unpacking WAS patches"
	tar -xpf ${localRepo}/${was8Patch} -C ${localRepo}/


	@echo "Downloading JDK 7"
	wget -O ${localRepo}/java_1.7_64_config.tar --quiet ${was8Repo}/jdk_1.7_64/java_1.7_64_config.tar
	wget -O ${localRepo}/java_1.7_64.tar --quiet ${was8Repo}/jdk_1.7_64/java_1.7_64.tar

patchtmp:
	wget -O ${localRepo}/${was8Dist} --quiet ${was8Repo}/${was8Patch}

download6:
	@echo
	@echo "Downloading WAS 6 distribution"
	@-mkdir ${localRepo}
	wget -O ${localRepo}/${was6Dist} --quiet ${was6Repo}/${was6Dist}

	@echo "Unpacking software"
	tar -xpf ${localRepo}/${was6Dist} -C ${localRepo}/

downloadwps6:
	@echo
	@echo "Downloading WPS 6 distribution"
	@-mkdir ${localRepo}
	wget -O ${localRepo}/${wps6Dist} --quiet ${wps6Repo}/${wps6Dist}

	@echo "Unpacking software"
	tar -xpf ${localRepo}/${wps6Dist} -C ${localRepo}/

	@echo "Downloading JDBC Drivers"
	wget -O ${localRepo}/${oracle10gJdbcDriver} --quiet ${oracle10gJdbcRepo}/${oracle10gJdbcDriver}

deploywps6apps:
	@echo "Downloading LBG WPS EAR's"
	@./downloadWpsEars.sh	
	@ @${WSACMD} -f deployWpsApps.py ${wps6AppList} ${localRepo} ${AppTargetClusterName}

downloadora:
	@echo
	@echo "Downloading 11g distribution"
	[ -s ${localRepo}/ora ] || mkdir -p ${localRepo}/ora 
	wget -O ${localRepo}/${oracle11gDist} --quiet ${oracle11gRepo}/${oracle11gDist}
	@echo "Unpacking software"
	tar -xpf ${localRepo}/${oracle11gDist} -C ${localRepo}/ora

	@# Also place a copy in tmp so that root user can locate
	[ -s /tmp/ora ] || mkdir /tmp/ora 
	tar -xpf ${localRepo}/${oracle11gDist} -C /tmp/ora

installora:
	@echo "Installing Oracle database"
	@#whoami | grep root || echo "ERROR - Must be logged in as root to install Oracle!!"

	-@sudo rpm -i /tmp/ora/bc-1.06.95-1.el6.x86_64.rpm
	-@sudo rpm -i /tmp/ora/libaio-0.3.107-10.el6.x86_64.rpm
	@sudo rpm -i /tmp/ora/oracle-xe-11.2.0-1.0.x86_64.rpm 
	@sudo /etc/init.d/oracle-xe configure responseFile=/tmp/ora/xe.rsp
	@sudo rpm -i /tmp/ora/oracle-instantclient11.2-basic-11.2.0.4.0-1.x86_64.rpm 
	@sudo rpm -i /tmp/ora/oracle-instantclient11.2-sqlplus-11.2.0.4.0-1.x86_64.rpm

uninstallora:
	@echo "Un-installing Oracle database"
	-@sudo rpm --erase oracle-instantclient11.2-sqlplus-11.2.0.4.0-1.x86_64
	-@sudo rpm --erase oracle-instantclient11.2-basic-11.2.0.4.0-1.x86_64
	-@sudo rpm --erase oracle-xe-11.2.0-1.0.x86_64

startora:
	@echo "Starting Oracle database"
	@sudo /etc/init.d/oracle-xe start

testora:
	@echo "Testing Oracle database status"
	@sudo /etc/init.d/oracle-xe status
	@./testOra.sh	
	@echo "Querying Oracle database"

	
stopora:
	@echo "Stopping Oracle database"
	@sudo /etc/init.d/oracle-xe stop

popora:
	@echo "Setting up Oracle database"
	@./populateOra.sh

salsalogging:
	@echo "Creating Salsa RPC log directory"
	@mkdir -p /tmp/salsa/logs/rpc/

logstash:
	@echo "Starting Logstash service"
	@sudo service logstash restart

deploysnoop:
	@echo "Deploying Snoop"
	@${WSACMD} -f deploySnoop.py ${clusterName} ${wasInstallDir}

deploysnoop6:
	@echo
	@echo "Deploying Default Application (snoop)"
	@${WSACMD} -f deploySnoop_v6.py ${clusterName} ${wasInstallDir}

vhost:
	@echo
	@echo "Configuring Virtual Host Aliases"
	@${WSACMD} -f vhost.py

wasliberty:
	@echo "Defining liberty profile in WAS - node is ${nodeName} and name is ${libertyProf}"
	-@${WSACMD} -f createLibertyProfile.py ${nodeName} ${libertyProf}
	@echo "Installing Liberty binaries"
	~/was/java/jre/bin/java -jar ~/repo/wlp-core-trial-runtime-8.5.5.2.jar --acceptLicense ~/was
	@echo "Creating concrete Liberty server"
	~/was/wlp/bin/server create ${libertyProf}
	

dmgr6:dmgr_v6.resp
	@echo
	@echo "Creating Deployment Manager profile"
	@${wasInstallDir}/bin/manageprofiles.sh -response dmgr_v6.resp
	@[ -s ${profilePath}/${dmgrProf} ]  || echo "ERROR: Deployment Manager profile has not been created, exiting!"

node6:node_v6.resp
	@echo
	@echo "Creating Node profile"
	@${wasInstallDir}/bin/manageprofiles.sh -response node_v6.resp
	@[ -s ${profilePath}/${nodeProf} ]  || echo "ERROR: Node profile has not been created, exiting!"

dmgrwps6:dmgr_wps_v6.resp
	@echo
	@echo "Creating WPS V6 Deployment Manager profile"
	@wget -O ${localRepo}/${oracle10gJdbcDriver} --quiet ${oracle10gJdbcRepo}/${oracle10gJdbcDriver}
	@${wasInstallDir}/bin/manageprofiles.sh -response dmgr_wps_v6.resp
	@[ -s ${profilePath}/${dmgrProf} ]  || echo "ERROR: Deployment Manager profile has not been created, exiting!"

nodewps6:node_wps_v6.resp
	@echo
	@echo "Creating WPS V6 Node profile"
	@${wasInstallDir}/bin/manageprofiles.sh -response node_wps_v6.resp
	@[ -s ${profilePath}/${nodeProf} ]  || echo "ERROR: Node profile has not been created, exiting!"

waspatch:
	echo "Installing WAS patches"
	${installDir}/im/eclipse/IBMIM -acceptLicense -input waspatch.resp -silent -nosplash


was6:
	@# NOTE: The was6 and wps6 (below) targets are identical however
	@# I've split them out for future flexibility 
	@echo
	@echo "Installing WAS6 binaries"
	cp was6.resp ${was6SrcDir}
	${was6SrcDir}/install -options was6.resp -silent

wps6:
	@echo
	@echo "Installing WAS6 binaries"
	cp was6.resp ${was6SrcDir}
	${was6SrcDir}/install -options was6.resp -silent


cluster6:
	@echo "Creating Cluster (V6)"
	@${WSACMD} -f createCluster_v6.py ${clusterName} ${clusterBasePort} ${nodeName}


startnode:
	@echo
	@echo "Starting Nodeagent"
	${wasInstallDir}/profiles/${nodeProf}/bin/startNode.sh

startdmgr:
	@echo
	@echo "Starting Deployment Manager"
	${wasInstallDir}/profiles/${dmgrProf}/bin/startManager.sh

stopnode:
	@echo
	@echo "Stopping Nodeagent"
	-@${wasInstallDir}/profiles/${nodeProf}/bin/stopNode.sh -user ${wasUser} -password ${wasPass}

stopdmgr:
	@echo
	@echo "Stopping Deployment Manager"
	-@${wasInstallDir}/profiles/${dmgrProf}/bin/stopManager.sh -user ${wasUser} -password ${wasPass}

stopclusters:
	@echo "Stopping Clusters"
	-@${WSACMD} -f stopClusters.py

startclusters:
	@echo "Starting Clusters"
	-@${WSACMD} -f startClusters.py

startclusterswps:
	@# Currently only works for single node implementations - Bob.C 18/07/14
	@echo "Starting WPS Clusters"
	-@${WSACMD} -f startClusters_wps.py ${MessagingClusterName} ${AppTargetClusterName} ${SupportClusterName} ${nodeName}


depenv:depenv.resp
	@echo "Generating Deployment Environment"
	@cp depenv.resp ${profilePath}/${envName}Dmgr
	@${WSACMD} -f genDepEnv.py ${envName} ${profilePath}/${envName}Dmgr/depenv.resp

setports:
	@echo
	@echo "Configuring TCP ports"
	@${WSACMD} -f setPorts.py ${envName} ${clusterBasePort} ${clusterName}

setportswps:
	@echo
	@echo "Configuring TCP ports"
	@${WSACMD} -f setPorts.py ${envName} ${appBasePort} ${AppTargetClusterName}
	@${WSACMD} -f setPorts.py ${envName} ${messBasePort} ${MessagingClusterName}
	@${WSACMD} -f setPorts.py ${envName} ${suppBasePort} ${SupportClusterName}

uninstalljee: stopall
	@echo "Uninstalling..."
	-@rm -r ${UNINST_DIRS} > /dev/null 2>&1
	@echo "Uninstall complete."

clean:
	-@rm -f *.resp *.xml *.ports

cleanup:
	@echo "Removing repository and temporary files"
	-@ rm -rf ${localRepo}
	-@ rm -r webservicelogs waslogs wbilogs responsefile*txt 

createds:
	@echo
	@${WSACMD} -f createDataSource.py ${cellName} "TestJdbcProvider" "Oracle" "bob" "password" "TestDS"

createjndient:
	@echo
	@${WSACMD} -f createJndiEntry.py salsaRep slr.service.url ${slr.service.url}
	@${WSACMD} -f createJndiEntry.py salsaRep cia.service.url ${cia.service.url}
	@${WSACMD} -f createJndiEntry.py salsaRep ipa.service.url ${ipa.service.url}
	@${WSACMD} -f createJndiEntry.py salsaRep fuse.service.url ${fuse.service.url}
	@${WSACMD} -f createJndiEntry.py salsaRep slr.service.timeout ${slr.service.timeout}
	@${WSACMD} -f createJndiEntry.py salsaRep slr.max.connections ${slr.max.connections}

