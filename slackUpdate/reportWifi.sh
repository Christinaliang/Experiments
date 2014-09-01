#/bin/bash

netDevice="wlan0"
pollTime=300

lastMsg=""

while true
do

	#Get the name of the wifi network.
	networkName=$(iwconfig $netDevice | grep 'ESSID:' | sed 's/.*ESSID://g' | sed 's/"//g' | sed 's/ *$//')

	#Get the ip of the machine
	ip=$(ifconfig wlan0 | sed -n -e 's/ *inet addr:\([0-9.]\+\).*/\1/gp')

	#Get the hostname of this machine
	name=$(hostname)

	#Construct the update message
	msg="$name has come online. It is on the network \"$networkName\" with the IP $ip"
	
	if [ "$msg" != "$lastMsg" ];
	then
		./slackUpdate.py "$msg"
		#echo $msg
	fi

	lastMsg=$msg
	sleep $pollTime

done
