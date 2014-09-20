#!/bin/sh

props=config.props
[ ! -s "$props" ] && echo "$0 : cannot find properties file $props" && exit 1
. ./"$props" > /dev/null 2>&1

SED=`which sed`

# Regex to look for strings surrounded with double underscores
pattern='(.*)__([A-Za-z0-9]*[^__])__(.*)'

# Set fileName for first pass in of file
fileName=$respDir/${1}
[ ! -s $fileName ] && echo "${0} ERROR: $fileName does not exist" && exit 1

newFile=${1}
echo "Creating response file : $newFile"
cp $fileName $newFile

flag=1

while [ $flag -eq 1 ]; do
  	grep -qE "$pattern" $newFile
  	if [ $? -ne 0 ]
	then
    		flag=0
    		chmod 755 $newFile
  	else
    		for item in $(grep -E "$pattern" $newFile | $SED -re "s:${pattern}:\2:") 
		do
			eval value=\${$item}
      			[ -z "$value" ] && echo "ERROR: Cannot set __${item}__ in $newFile" && break 2
      			eval $SED -e "s:__${item}__:\${value}:" $newFile > $newFile.tmp
      			mv $newFile.tmp $newFile	
    		done
  	fi
done
