#! /usr/bin/env python
import requests
from bs4 import BeautifulSoup

account={
        "username":"520095417@qq.com",
        "password":"z4326959"
        }


def getLoginlt (cookies):
    print 'getLoginlt'
    print cookies
    headers={
        "Connection": "keep-alive",
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36"
            }
    headers['Cookie']=cookies
    r=requests.get('https://www.umeng.com/sso/login',headers=headers,timeout=5)
    print r.headers
    html=r.text
    soup=BeautifulSoup(html)
    form=soup.findAll(['input'])
    for item in form:
        if item.get('id')=='lt':
            value=item.get('value')
            return value


def login (lt,account,cookies):
    print 'login'
    headers={
            "Connection": "keep-alive",
            "Content-Type":"application/x-www-form-urlencoded" ,
            "Content-Language":"zh-cn",
            }
    headers['Cookie']=cookies
    data={}
    data['username']=account['username']
    data['password']=account['password']
    data['lt']=lt
    data['service']="http://www.umeng.com/users/login_redirect"
    print data
    r=requests.post('https://www.umeng.com/sso/login',data=data,headers=headers,timeout=5)
    print r.headers
    #print r.text
    print r.status_code
    cookie=r.cookies
    for keys in cookie.keys():
        print cookie[keys]


def api_get ():
    print 'api_get'
    r=requests.get('http://www.umeng.com/apps/8a6100022fb042652b42f535/events/load_table_data?page=1&versions%5B%5D=&stats=count&per_page=50&show_all=false '\
            ,headers=headers)
    res=r.json()
    lists=res['stats']
    print len(lists)
    for item in lists:
        count=item['count']
        count_today=item['count_today']
        name=item['name']
        display_name=item['display_name']
        print "%-25s,%-10s,%-10s,%-10s"%(display_name,count,count_today,name)

def getCookie ():
    print 'getCookie'
    r=requests.get('http://www.umeng.com',timeout=5)
    #print r.text
    content=r.headers['set-cookie']
    print content
    return content


def main():
    print 'main'
    cookie=getCookie()
    #if cookie:
        #lt=getLoginlt(cookie)
    #else:
        #print 'cookie is None,exit'
    #if lt and cookie:
        #login(lt,account,cookie)
    #else:
        #print "lt is None ,exit"
        #return


if __name__ == '__main__':
    main()
