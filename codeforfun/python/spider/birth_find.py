#! /usr/bin/env python
#coding:utf8
import requests
from bs4 import BeautifulSoup
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def get(count):
    url='http://www.douban.com/group/topic/30388571/?start='
    url+=str(count*100)
    try:
        response=requests.get(url,timeout=20)
    except:
        print 'error'
        return
    html=response.text
    soup=BeautifulSoup(html)
    lis=soup.findAll('li',class_='clearfix comment-item')
    i=0
    for item in lis:
        handle(item,count,i)
        i+=1
    print '%s finish'%(str(count))


def handle(Item,page,num):
    content=Item.p.string
    content=str(content)
    content=content.strip()
    if '1105' in content:
        print 'content %s page = %s num = %s'%(content,page,num)
    elif '11月5' in content:
        print 'content %s page = %s num = %s'%(content,page,num)
    elif '11月05' in content:
        print 'content %s page = %s num = %s'%(content,page,num)
    elif '11.5' in content:
        print 'content %s page = %s num = %s'%(content,page,num)
    elif '11.05' in content:
        print 'content %s page = %s num = %s'%(content,page,num)


def main():
    for i in xrange(178):
        get(i)

if __name__ == '__main__':
    main()
