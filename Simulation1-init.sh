#!/bin/bash

nmcli nm wifi off
rfkill unblock wlan
hostapd hostap/hostapd/hostapd.conf &
echo Process ID: $!
ifconfig wlan0 10.0.0.254 netmask 255.255.255.0
ovs-vsctl add-port s1 wlan0
