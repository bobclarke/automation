import sys
envName=sys.argv[0]
responseFile=sys.argv[1]

AdminTask.importDeploymentEnvDef(['-filePath',responseFile,'-topologyName',envName])
AdminConfig.save()

AdminTask.generateDeploymentEnv(['-topologyName',envName])
AdminConfig.save()
