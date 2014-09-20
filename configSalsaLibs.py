# salsaSharedLibs.py
# Author: Bob Clarke
# Date: 04/06/2014

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set up
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import sys
cluster=sys.argv[0]
libName=sys.argv[1]
cell=sys.argv[2]
warName=sys.argv[3]
nodeProfile=sys.argv[4]
moduleName=sys.argv[5]
sharedLibCp=sys.argv[6]
appName=sys.argv[7]

# Import wsadminlib.py
execfile('../script/wsadmin/wsadminlib.py')


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Subs 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def createSharedLib(libName, classpath, isolated):
        print '<BUILD>: Creating ' +libName
        clusterId = AdminConfig.getid('/ServerCluster:'+cluster+'/')
        out = AdminConfig.create('Library', clusterId,   [['name', libName], ['classPath', classpath], ['isolatedClassLoader', isolated]])
        print '<RESULT>: '+out

def genClassPath(sharedLibCp):
        print '<BUILD>: Generating classpath for ' +libName
        #base='${WAS_INSTALL_ROOT}/profiles/'+nodeProfile+'/installedApps/'+cell+'/'+moduleName+'.ear/'+warName+'/WEB-INF/lib/'
        base='/root/was/profiles/'+nodeProfile+'/installedApps/'+cell+'/'+moduleName+'.ear/'+warName+'/WEB-INF/lib/'
        classPath = ''
        #for jar in sharedLibCp.split(';'):
        jars = sharedLibCp.split(';')
        jars.pop()
        count=1
        for jar in jars:
                if(len(jars) == count):
                        #classPath += base+jar+';'
                        classPath += base+jar
                else:
                        classPath += base+jar+';'
                count = count+1

        print classPath
        return(classPath)

def linkSharedLibs():
        print 'Linking module '+warName+ ' to shared library '+libName
        AdminApp.edit(appName, ['-MapSharedLibForMod', [[appName, '.*', libName]]])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

classPath=genClassPath(sharedLibCp)
#createSharedLibraryIsolated(libName, classPath, 'true')
createSharedLib(libName, classPath, 'true')
associateSharedLibrary(libName, appName, '')

AdminConfig.save()
