#! /usr/bin/env python
#coding:utf8
import random

def init(number):
    result=[x for x in range(int(number))]
    return result

def root(array,index):
    while array[index] != index:
        index=array[index]
    return array[index]

def union(array,index_a,index_b):
    if(connected(array,index_a,index_b)):
        return array
    else:
        root_b=root(array,index_b)
        array[index_a]=root_b
        return array


def connected(array,index_a,index_b):
    root_a=root(array,index_a)
    root_b=root(array,index_b)
    return root_a==root_b

def main():
    size=10
    array=init(size)
    #print array
    for i in xrange(size/2):
        rand_a=random.randint(0,size-1)
        rand_b=random.randint(0,size-1)
        print 'union %d and %d'%(rand_a,rand_b)
        array=union(array,rand_a,rand_b)
    print array
    print connected(array,1,2)
    print connected(array,2,4)
    print connected(array,4,8)
    print connected(array,3,7)

if __name__ == '__main__':
    main()
