#!/bin/bash
#edit by Zjj
apk=$1
file=$2

apktool(){
    echo
    echo "doing apktool...."
    echo
    apktool d $apk $file
}

class2jar(){
    echo
    echo "unzip classes.dex ..."
    echo
    unzip $apk classes.dex
    echo
    echo "unzip dex2jar classes.dex ..."
    echo
    ~/Documents/mytools/apktool/dex2jar/dex2jar.sh classes.dex
    rm classes.dex
    mv classes_dex2jar.jar $file/$apk.jar
}

apktool 
class2jar
