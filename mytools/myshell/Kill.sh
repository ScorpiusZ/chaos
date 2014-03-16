#!/bin/sh

echo "terminate $1"
ps aux|grep $1|grep -v grep
kill $(ps aux| grep $1|grep -v grep|cut -c 9-15)
