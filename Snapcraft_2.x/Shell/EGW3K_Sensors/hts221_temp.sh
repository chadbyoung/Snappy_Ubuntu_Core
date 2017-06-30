#!/bin/bash
# This script uses the ST Micro HTS221 sensor
# that is located on the Dell Edge Gateway 300x 
# series IOT devices

raw=`sudo cat /sys/bus/iio/devices/iio\:device0/in\_temp\_raw`
offset=`sudo cat /sys/bus/iio/devices/iio\:device0/in\_temp\_offset`
scale=`sudo cat /sys/bus/iio/devices/iio\:device0/in\_temp\_scale`

echo $raw
echo $offset
echo $scale

temp=($raw+$offset)*$scale

echo ""
echo $temp
echo ""
