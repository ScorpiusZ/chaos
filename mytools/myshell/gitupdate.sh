#!/bin/sh
#edit by Zjj

if [ "$1" == "pull" ]; then
    cd ~/.vim
    git pull origin master
    cd ~/.myrc
    git pull origin master
    cd ~/Documents/githubs/chaos
    git pull origin master
elif [ "$1" == "push" ]; then
    cd ~/.vim
    git add -A
    git commit -a
    git pull origin master
    cd ~/.myrc
    git add -A
    git commit -a
    git pull origin master
    cd ~/Documents/githubs/chaos
    git add -A
    git commit -a
    git pull origin master
else
    echo " options [pull|push] "
    echo "pull : pull everything from master"
    echo "push : push everything from master"
fi
