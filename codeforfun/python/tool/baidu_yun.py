#! /usr/bin/env python
#coding:utf8
import requests
from time import sleep
import sys

def get_share_list(uk,page,per):
    url='http://yun.baidu.com/share/homerecord?uk={0}&page={1}&pagelength={2}'.format(uk,page,per)
    print url
    result=requests.get(url)
    return result.json()

def get_commic(uk,commic_name):
    stop=False
    result=[]
    page=1
    while not stop:
        data=get_share_list(uk,page,10)
        if data['list']:
            for item in data['list']:
                if commic_name in item['typicalPath'].encode('utf-8'):
                    show_share_info(uk,item)
                    result.append(item)
        else:
            stop = True
        page+=1
        sleep(1)
    return result

def share_url(uk,share_id):
    return 'http://pan.baidu.com/wap/link?uk={0}&shareid={1}&third=0'.format(uk,share_id)

def show_share_info(uk,item):
    print '{0} , share_url = {1}'.format(item['typicalPath'].encode('utf-8'),share_url(uk,item['shareId']))

def main():
    get_commic('789356580','蜡笔小新')



if __name__ == '__main__':
    main()
