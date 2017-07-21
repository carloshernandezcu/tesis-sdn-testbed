#!/bin/bash

#service network-manager stop
#ifconfig eth0 up
#ifconfig eth1 up
#dhclient
ifconfig wlan0 up
sleep 2
nmcli nm wifi off
rfkill unblock wlan
#rfkill unblock wifi
#rfkill unblock all
sleep 2
hostapd hostap/hostapd/hostapd.conf &
echo Process ID: $!
ifconfig wlan0 10.0.0.254 netmask 255.255.255.0
ovs-vsctl add-port s1 wlan0
