#! /usr/bin/env python
#coding:utf8

#  判断身份证号是否合法
def validId(Iid):
    powers=('7','9','10','5','8','4','2','1','6','3','7','9','10','5','8','4','2')
    parityBits=('1','0','X','9','8','7','6','5','4','3','2')
    parityBit=Iid[-1]
    ids=map(int,Iid[0:17])
    index=int(sum([a*b for a,b in zip(ids,map(int,powers))])%11)
    if parityBits[index]==parityBit:
        return True
    else:
        return False



