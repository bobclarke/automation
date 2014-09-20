# populateOra.sh
# Author: Bob Clarke
# Date: 06/08/2014

# Setup 
props=config.props
[ ! -s "$props" ] && echo "$0 : cannot find properties file $props" && exit 1
. ./"$props" > /dev/null 2>&1

export LD_LIBRARY_PATH
export ORACLE_SID
export ORACLE_HOME
SQLPLUSCMD=${LD_LIBRARY_PATH}/../bin/sqlplus

# Create/clear the sql.log
cat /dev/null > sql.log

# Drop stuff 
$SQLPLUSCMD system/${oraSysPw}@${ORACLE_SID} @db_drop_users.resp | tee -a sql.log
$SQLPLUSCMD system/${oraSysPw}@${ORACLE_SID} @db_drop_tablespaces.resp | tee -a sql.log

# Create stuff
$SQLPLUSCMD system/${oraSysPw}@${ORACLE_SID} @db_create_tablespaces.resp | tee -a sql.log
$SQLPLUSCMD system/${oraSysPw}@${ORACLE_SID} @db_create_users.resp | tee -a sql.log
$SQLPLUSCMD system/${oraSysPw}@${ORACLE_SID} @db_common_tables.resp | tee -a sql.log
$SQLPLUSCMD system/${oraSysPw}@${ORACLE_SID} @db_bpe_tables.resp | tee -a sql.log
$SQLPLUSCMD system/${oraSysPw}@${ORACLE_SID} @db_scasys_tables.resp | tee -a sql.log
$SQLPLUSCMD system/${oraSysPw}@${ORACLE_SID} @db_bpeme_tables.resp | tee -a sql.log
$SQLPLUSCMD system/${oraSysPw}@${ORACLE_SID} @db_bsp_tables.resp | tee -a sql.log
$SQLPLUSCMD system/${oraSysPw}@${ORACLE_SID} @db_scaapp_tables.resp | tee -a sql.log
$SQLPLUSCMD system/${oraSysPw}@${ORACLE_SID} @db_ceime_tables.resp | tee -a sql.log
$SQLPLUSCMD system/${oraSysPw}@${ORACLE_SID} @db_obs_tables.resp | tee -a sql.log
