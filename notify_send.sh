#!/bin/bash

user=$1 # this user will receive notification
echo $2 > /tmp/topic
echo $3 > /tmp/desc

runuser -l $user -c 'eval "export (egrep -z DBUS_SESSION_BUS_ADDRESS /proc/(pgrep -u $LOGNAME gnome-session)/environ)" && notify-send (cat /tmp/topic) (cat /tmp/desc)'

rm /tmp/topic /tmp/desc
