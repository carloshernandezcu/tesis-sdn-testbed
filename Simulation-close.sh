#!/bin/bash

echo "*** Stop Access-Point from USB dongle"
killall hostapd
ifconfig wlan0 down

echo "*** Clear Mininet configurations"
mn -c

echo "*** Clear CLI"
clear
