# abc.py
# Author: Bob Clarke
# Date:

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Define subs
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def serverNamespace(ns,rl):
	file = open('/tmp/jndi.file','a')
	s=ns.split('=')[2]
	roots = ['tree','host','legacy','cell','node','server','default']
	for root in roots:
		opts = '[[-root '+root+' -report long]]'
		file.write('\n\nSERVER is: '+s+' ROOT IS: '+root)
		file.write( AdminControl.invoke(ns, 'dumpServerNameSpace', opts))
	file.flush()

def localNamespace(ns,rl):
	file = open('/tmp/jndi.file','a')
	s=ns.split('=')[2]
	opts = '[[-report '+ rl +']]'
	file.write('\n\nSERVER is: '+s)
	file.write( AdminControl.invoke(ns, 'dumpLocalNameSpace', opts))
	file.flush()

def javaNamespace(ns,rl):
	file = open('/tmp/jndi.file','a')
	s=ns.split('=')[2]
	roots = ['tree','host','legacy','cell','node','server','default']
	for root in roots:
		#opts = '[[-root '+root+' -report long]]'
		#opts = '[[DefaultApplication] [DefaultWebApplication.war] ["Snoop Servlet"] ["-report long"]]'
		opts = '[[DefaultApplication] [DefaultWebApplication.war] ["Snoop Servlet"] ["-report long"]]'
		file.write('\n\nSERVER is: '+s+' ROOT IS: '+root)
		file.write( AdminControl.invoke(ns, 'dumpJavaNameSpace', opts))
		#print AdminControl.invoke(ns, 'dumpJavaNameSpace', opts)
		print AdminControl.invoke(ns, "dumpJavaNameSpace", '[DefaultApplication DefaultWebApplication.war "Snoop Servlet" "-report long"]')
	file.flush()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Setup
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Create empty file 
open('/tmp/jndi.file', 'w').close()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main program
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

for ns in AdminControl.queryNames('type=NameServer,*').splitlines():
	#serverNamespace(ns, 'long')
	#localNamespace(ns, 'long')
	javaNamespace(ns, 'long')



# execfile('/home/vmfest/salsa-poc/infrastructure/websphere-automation/dumpJndiEntries.py')
