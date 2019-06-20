#!/bin/bash

user=$1 # this user will receive notification
echo $2 > /tmp/topic
echo $3 > /tmp/desc

if [ "$(getent passwd $user | awk -F: '{ print $7 }')" == "/usr/bin/fish" ]; then
	runuser -l $user -c 'eval "export (egrep -z DBUS_SESSION_BUS_ADDRESS /proc/(pgrep -u $LOGNAME gnome-session)/environ)" && notify-send (cat /tmp/topic) (cat /tmp/desc)'
else
	runuser -l $user -c 'eval "export $(egrep -z DBUS_SESSION_BUS_ADDRESS /proc/$(pgrep -u $LOGNAME gnome-session)/environ)" && notify-send $(cat /tmp/topic) $(cat /tmp/desc)'
fi

rm /tmp/topic /tmp/desc
