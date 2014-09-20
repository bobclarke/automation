# testOra.sh -x
# Author: Bob Clarke
# Date: 06/08/2014

props=config.props
[ ! -s "$props" ] && echo "$0 : cannot find properties file $props" && exit 1
. ./"$props" > /dev/null 2>&1

export LD_LIBRARY_PATH
export ORACLE_SID
export ORACLE_HOME
echo $LD_LIBRARY_PATH
echo $ORACLE_SID
echo $ORACLE_HOME

${LD_LIBRARY_PATH}/../bin/sqlplus system/oracle@XE << EOF
select username from dba_users;
exit
EOF
