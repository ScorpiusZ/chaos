#!/bin/bash
#edit by Zjj

mode=$(gsettings get org.gnome.system.proxy mode)
mode=$(echo $mode | tr -d \'\\\'\')
echo "Present mode is : $mode"

if [[ $mode == "none" ]]; then
    echo "set manula proxy mode"
    gsettings set org.gnome.system.proxy mode 'manual' 
    gsettings set org.gnome.system.proxy.http host '127.0.0.1'
    gsettings set org.gnome.system.proxy.http port 8087
    gsettings set org.gnome.system.proxy.https host '127.0.0.1'
    gsettings set org.gnome.system.proxy.https port 8087
    source ~/Documents/githubs/chaos/mytools/myshell/GoAgent.sh
else
    echo "set none proxy mode"
    gsettings set org.gnome.system.proxy mode 'none' 
fi

