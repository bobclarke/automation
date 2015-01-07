# dynaCacheMon.py
# Author: Bob Clarke 
# Date: 05/01/2015
#

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set up
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import time
count = 0
month = time.ctime().split()[1]
day = time.ctime().split()[2]
year = time.ctime().split()[4]
timeStamp = time.ctime().split()[3]
logFile='/tmp/dynaCacheMon_'+timeStamp+'_'+month+'_'+day+'_'+year+'.log'
file = open(logFile,'a')

if(len(sys.argv) == 2):
	maxLoops = float(sys.argv[0])
	waitTime = float(sys.argv[1])
else:
	# Default values
	maxLoops = 3
	waitTime = 10

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main program
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print '\nRunning '+str(maxLoops)+' loops with '+str(waitTime)+' seconds delay. Logging results to '+logFile

while (count < maxLoops):
        print "Loop number "+str(count)
        mBeans = AdminControl.queryNames('type=DynaCache,*')
        for mBean in mBeans.splitlines():
                process = mBean.split(',')[1]
		jvm = AdminControl.queryNames('type=JVM,'+process+',*')
		freeHeap = AdminControl.invoke(jvm, 'getFreeMemory')
		maxHeap = AdminControl.invoke(jvm, 'getMaxMemory')
		file.write('------------------- JVM Details --------------------\n')
		file.write('Loop: '+str(count)+'\n')
		file.write('Time: '+str(time.ctime())+'\n')
		file.write('JVM: '+process+'\n')
		file.write('Max heap: '+maxHeap+'\n')
		file.write('Free heap: '+freeHeap+'\n')
		file.write('---------- Cache instances for this JVM ------------\n')

                for cacheInstance in AdminControl.invoke(mBean, 'getCacheInstanceNames').splitlines():
                        #stats = AdminControl.invoke(mBean, 'getCacheStatistics', cacheInstance+' [MemoryCacheSizeInMB  MemoryCacheEntries]')
			stats = AdminControl.invoke(mBean, 'getAllCacheStatistics', cacheInstance)
                        file.write('### Instance Name: '+cacheInstance+' ###\n')
                        file.write(stats+',\n\n')
        file.flush()
        count = count+1
        sleep(waitTime)
file.close()

# execfile('/home/clarkeb/automation/dynaCacheMon.py')
