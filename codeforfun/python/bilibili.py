#! /usr/bin/env python
#ecoding=utf-8
import re

def getDate ():
    f=file('bilibili.dat')
    i=1
    for line in f.readlines():
        print line
        if re.findall("\?",line):
            part=line.split('?')
        elif re.findall("\？",line):
            part=line.split('？')
        else:
            part=None
        if part:
            for pos in range(len(part)):
                print part[pos]
        i+=1
        if i>10:
            break

def main ():
    getDate()

if __name__=='__main__':
    main()
