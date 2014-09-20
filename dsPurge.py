for ds in AdminControl.queryNames('type=DataSource,*').splitlines():
        name = AdminControl.invoke(ds, 'getName')
        jndi = AdminControl.invoke(ds, 'getJndiName')
        status = AdminControl.invoke(ds, 'getStatus')
        if( status.find("99") <= -1 and name.find("OTiSDataSource") <= -1):
                print "DS name: "+name+" jndi: "+jndi+" status "+status
                #AdminControl.invoke(ds, 'purgePoolContents("immediate")')
                AdminControl.invoke(ds, 'purgePoolContents()')
