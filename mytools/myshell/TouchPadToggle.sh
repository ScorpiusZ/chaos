#!/bin/bash
#edit by Zjj

ison=$(synclient|grep Touchpad |cut -d '=' -f 2|tr -d ' ')
if [ "$ison" == "1" ]; then
    synclient Touchpadoff=0
else
    synclient Touchpadoff=1
fi
