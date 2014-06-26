#!/bin/bash
#edit by Zjj

if [ "$1" == "pull" ]; then
    cd ~/.vim
    git pull --ff-only origin master
    cd ~/.myrc
    git pull --ff-only origin master
    cd ~/Documents/githubs/chaos
    git pull --ff-only origin master
elif [ "$1" == "push" ]; then
    cd ~/.vim
    git add -A
    git commit -a
    git push origin master
    cd ~/.myrc
    git add -A
    git commit -a
    git push origin master
    cd ~/Documents/githubs/chaos
    git add -A
    git commit -a
    git push origin master
elif [ "$1" == "status" ]; then
    cd ~/.vim
    echo 
    echo "~/.vim   ::"
    echo 
    git status
    echo 
    echo "~/.myrc   ::"
    echo 
    cd ~/.myrc
    git status
    echo 
    echo "~/Documents/githubs/chaos     ::"
    echo 
    cd ~/Documents/githubs/chaos
    git status
else
    echo " options [pull|push] "
    echo "pull : pull everything from master"
    echo "push : push everything from master"
fi
