for cluster in AdminControl.queryNames('type=Cluster,*').splitlines():
	AdminControl.invoke(cluster, 'stop')
