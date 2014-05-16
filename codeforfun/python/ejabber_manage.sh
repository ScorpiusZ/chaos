#!/bin/bash
#edit by Zjj

registe(){
    echo "registe"
    #ejabberdctl  register xiaopu 115.29.173.123 blue1207
    #ejabberdctl  register 小美 115.29.173.123 blue1207
    #ejabberdctl  register 小蕾 115.29.173.123 blue1207
    #ejabberdctl  register 小琪 115.29.173.123 blue1207
    #ejabberdctl  register 小兰 115.29.173.123 blue1207
}

help(){
    echo "Usage: $name clean"
}

clean(){
    echo "ejabberdctl stop"
    #ejabberdctl stop
    echo "cleaning......"
    echo "rm -f /var/lib/ejabberd/*"
    #rm -f /var/lib/ejabberd/*
    echo "ejabberdctl start"
    #ejabberdctl start
}

add_share_roster(){
    echo "add_share_roster"
    echo "add group"
    #ejabberdctl srg_create cs_team 115.29.173.123 cs_team cs_team everybody
    #ejabberdctl srg_create everybody 115.29.173.123 everybody everybody cs_team
    echo "add user to groups"
    #ejabberdctl srg_user_add 小美 115.29.173.123  cs_team 115.29.173.123 
    #ejabberdctl srg_user_add 小兰 115.29.173.123  cs_team 115.29.173.123 
    #ejabberdctl srg_user_add 小蕾 115.29.173.123  cs_team 115.29.173.123 
    #ejabberdctl srg_user_add 小琪 115.29.173.123  cs_team 115.29.173.123 
    #ejabberdctl srg_user_add @online "" everybody 115.29.173.123
    echo "current shared roster list:"
    #ejabberdctl srg_list 115.29.173.123
}

name=$0
command=$1
if [ $command = "help" ]; then
    help
fi
if [ $command = "clean" ]; then
    clean
    registe
    add_share_roster
fi

