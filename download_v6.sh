#!/bin/bash

# download.sh
# Author: Bob Clarke
# Date: 05/06/2014
# NOTE: I need to make the tidySubdirs function much better 
# or better still, fix the download target so that I don't 
# need it)

#---------------------------------------------------------------------
# Setup 
#---------------------------------------------------------------------
props=config.props
[ ! -s "$props" ] && echo "$0 : cannot find properties file $props" && exit 1
. ./"$props" > /dev/null 2>&1

#---------------------------------------------------------------------
# Functions  
#---------------------------------------------------------------------
message()
{
        echo "<BUILD> $1"
}

checkDeps()
{
	# Is wget installed and in the path
	which wget > /dev/null 2>&1
	if [ $? -ne 0 ]; then 
		message "wget not installed or not in path, exiting!"
		exit 1
	fi

	# Sort out the download directory
	download_dir=~/.repo
	message "Creating directory ${download_dir}"
	if [ -d ${download_dir} ]; then
		message "${download_dir} directory exists"
	else
		mkdir -p ${download_dir}
	fi
}

getDist()
{
	message "Downloading app server image ${was6Image} from $remoteRepo"
	cd $download_dir
	wget --quiet --no-clobber ${remoteRepo}/${was6Image}
}


#---------------------------------------------------------------------
# Main  
#---------------------------------------------------------------------
checkDeps
getDist
