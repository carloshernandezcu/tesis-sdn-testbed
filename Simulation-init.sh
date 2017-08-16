#!/bin/bash

echo "*** Start USB dongle as Access Point"
ifconfig wlan0 up
nmcli nm wifi off
rfkill unblock wlan
hostapd tesis-sdn-testbed/hostapd/hostapd.conf &
ifconfig wlan0 10.0.0.254 netmask 255.255.255.0
