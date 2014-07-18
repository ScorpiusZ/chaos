#! /usr/bin/env python
#coding:utf8
import requests
from bs4 import BeautifulSoup
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

mode=True
def get(count,url):
    url+='?start='+str(count*100)
    try:
        response=requests.get(url,timeout=20)
    except:
        print 'error'
        return
    html=response.text
    soup=BeautifulSoup(html)
    lis=soup.findAll('li',class_='clearfix comment-item')
    if not lis or not len(lis):
        return False
    i=0
    for item in lis:
        handle(item,count,i)
        i+=1
    print '%s finish'%(str(count))
    return True


def handle(Item,page,num):
    content=Item.p.string
    content=str(content)
    content=content.strip()
    filter_content(content,page,num)

def filter_content(content,page,num):
    filters=getfilter()
    isPass=False
    for filter_item in filters:
        if not filter_item:
            continue
        if filter_item in content:
            isPass=True
            if not mode:
                break
        else:
            if mode:
                isPass=False
                break;
    if isPass:
            print 'content %s page = %s num = %s'%(content,page,num)


def getfilter():
    filters=[]
    with open('filter','r') as filter_file:
        contents=filter_file.read().split('\n')
        for line in contents:
            filters.append(line)
    return filters

def main():
    url=sys.argv[1]
    i=0
    while get(i,url):
        i=i+1

if __name__ == '__main__':
    main()
