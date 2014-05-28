#! /usr/bin/env python
#coding:utf8
from random import random

def inc(x):
    def incx(y):
        return x+y
    return incx

def demoinc():
    #demo of inc
    inc2=inc(2)
    print inc2(3)
    print inc(10)(20)

def demomap():
    name_List=["hao","chen","hahaha"]
    name_len=map(len,name_List)
    print name_len
    def toUpper(item):
        return item.upper()
    upper_name=map(toUpper,name_List)
    print upper_name
    print map(lambda x:x.lower(),upper_name)

def demonreduc():
    num_list=[1,2,3,4,5,6]
    print reduce(lambda x,y:x+y,num_list)
    print reduce(lambda x,y:x+y,map(lambda x:-x,num_list))
    print reduce(lambda x,y:x+y,num_list)/float(len(num_list))

def try_move(car_positions):
    def move_car(car_pos):
        return car_pos+1 if  random()>0.3 else car_pos
    res=map(move_car,car_positions)
    print res
    return res

def draw(car_positions):
    def draw_car(num):
        print "-"*num
    map(draw_car,car_positions)
    print

def movecar():
    time=5
    carnum=3
    car_positions=[1]*carnum
    while time:
        car_positions=try_move(car_positions)
        draw(car_positions)
        time-=1

def main():
    movecar()


if __name__ == '__main__':
    main()
