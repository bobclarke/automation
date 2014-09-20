# enableSec.py
# Author: Bob Clarke 
# Date: 27/06/2014
#
# Enables application security (NOTE: Administrative security is pre-enabled at DMGR profile creation time)

sec = AdminConfig.getid('/Security:/')
AdminConfig.modify(sec,[['appEnabled','true']])
AdminConfig.save()
