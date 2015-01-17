#! /usr/bin/env python
#coding:utf8
import os

def getLogDir():
    return getConfigs().get('log_dir','')

def getCsvDir():
    return getConfigs().get('csv_dir','')

def getConfigs():
    fileName=os.path.abspath(os.path.dirname(__file__))+'/configs/config'
    with open(fileName,'r') as configFile:
        return eval(configFile.read())

def main():
    print getConfigs()
    print getCsvDir()
    print getLogDir()

if __name__ == '__main__':
    main()
