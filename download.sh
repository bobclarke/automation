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

tidySubdirs()
{
	# Added this because I couldn't work out how to make wget put 
	# downloaded files in the correct place. To be fixed 
	longPath=`echo $1 | sed s/'http:\/\/'//`
	for war in `find $longPath -name '*.war'`
	do
		mv ${war} $2
	done
	for tar in `find $longPath -name '*.tar'`
	do
		mv ${tar} $2
	done
	for targz in `find $longPath -name '*.gz'`
	do
		mv ${targz} $2
	done
	for zip in `find $longPath -name '*.zip'`
	do
		mv ${zip} $2
	done
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
	message "Creating directory ${download_dir}/im"
	if [ -d ${download_dir}/im ]; then
		message "${download_dir}/im directory exists"
	else
		mkdir -p ${download_dir}/im
	fi
}

getIm()
{
	# We have to download and unpack IM (It's better for your saniity if you don't ask why, 
	# I barely held on to mine durring the 8 hours in which I tried to make this elegent and normal.)
	message "Downloading and unpacking IM from $remoteImRepo"
	cd $download_dir/im
	wget --quiet --no-parent --no-clobber --recursive --level=1 $remoteImRepo
	tidySubdirs $remoteImRepo $download_dir/im
	for zip in `ls *.zip`
	do
		unzip -o $zip  > /dev/null 2>&1
	done
}

getDist()
{
	# Get everything else
	message "Downloading and unpacking app server from $remoteRepo"
	cd $download_dir

	wget --quiet --no-parent --no-clobber --recursive --level=3 $remoteRepo

	tidySubdirs $remoteRepo $download_dir

	for tar in `ls *.tar*`
	do
		tar xvpf $tar > /dev/null 2>&1
		tar xvpzf $tar > /dev/null 2>&1
	done

}


#---------------------------------------------------------------------
# Main  
#---------------------------------------------------------------------
checkDeps
getIm
getDist

