#!/bin/sh
#edit by Zjj

files=$(ls | grep -v ".*\..*")
for file in $files
do
    if [ -e $HOME/.$file ]
    then
        echo "$HOME/.$file exist"
    else
        ln $file $HOME/.$file
        echo "create $HOME/.$file"
fi
done
