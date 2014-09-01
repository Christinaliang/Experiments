#/bin/bash

netDevice="wlan0"
pollTime=5

lastMsg=""

while true
do

	#Get the name of the wifi network.
	networkName=$(iwconfig $netDevice | grep 'ESSID:' | sed 's/.*ESSID://g' | sed 's/"//g' | sed 's/ *$//')

	#Get the ip of the machine
	ip=$(ifconfig wlan0 | sed -n -e 's/ *inet addr:\([0-9.]\+\).*/\1/gp')

	#Get the hostname of this machine
	name=$(hostname)

	#Constuct the update message
	msg="$name has come online. It is on the network \"$networkName\" with the IP $ip"
	
	if ["$msg" == "$lastMsg"];
	#if test $msg != $lastMsg
	then
		echo $msg
	fi

	lastMsg=$msg
	sleep $pollTime

done
