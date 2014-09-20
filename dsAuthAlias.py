# WIP

import sys

# Datasource - reflects change to Component-managed authentication alias 
AdminConfig.modify('(cells/localhostNode01Cell/nodes/localhostNode01/servers/server1|resources.xml#DataSource_1378290943613)', '[[name "mmdb"] [authDataAlias "localhostNode01/test"] [datasourceHelperClassname "com.ibm.websphere.rsadapter.Oracle10gDataStoreHelper"] [description "Data source template"] [category ""] [jndiName "jdbc/mmdb"] [xaRecoveryAuthAlias ""]]') 

# Mapping Module - reflects change to Container-managed authentication alias
AdminConfig.modify('(cells/localhostNode01Cell/nodes/localhostNode01/servers/server1|resources.xml#MappingModule_1378290943688)', '[[authDataAlias "localhostNode01/test"] [mappingConfigAlias "DefaultPrincipalMapping"]]')

