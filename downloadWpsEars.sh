# downloadWpsEars.sh
# Author: Bob Clarke
# Date: 22/08/2014

# Setup 
props=config.props
[ ! -s "$props" ] && echo "$0 : cannot find properties file $props" && exit 1
. ./"$props" > /dev/null 2>&1

wsCmd="${wasInstallDir}/profiles/${dmgrProf}/bin/wsadmin.sh -lang jython -user ${wasUser} -password ${wasPass}"

for ear in $wps6AppList
do
	echo "Downloading $ear"
	wget -O ${localRepo}/${ear} --quiet ${wps6AppRepo}/${ear}
done
