#! /usr/bin/env python
#coding:utf8
import requests
import MySQLdb
import datetime
import sys

db=MySQLdb.connect(host='localhost',user='root',passwd='',port=3306,db='test',charset='utf8')

def Exist(data):
    if not data:
        return False
    sql='select * from contents where source_id=%s'%data['source_id']
    cursor=db.cursor()
    count=cursor.execute(sql)
    if count==1:
        return True
    else:
        return False

def push2Db(data):
    if Exist(data):
        print '%s Exist'%data['source_id']
        return
    cursor=db.cursor()
    sql='insert into\
        contents(user_avatar,user_name,text,image,width,height,forward_count,\
        likes_count,unlikes_count,source_id,updated_at,created_at)\
        values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    try:
        cursor.execute(sql,
                [data['avatar'], data['name'],
                data['text'],data['image'] ,data['width']
                ,data['height'] ,data['forward'],data['likes_count']
                ,data['unlikes_count'],data['source_id']
                ,data['updated_at'] ,data['created_at']])
        db.commit()
        cursor.close()
    except:
        print 'error'
        cursor.close()
        return

def formatId(id):
    if id>999999999:
        id=int(id)%1000000000
        print 'id = %d'%id
    return id

def parseData(item,channel):
    data={}
    try:
        if channel=='bdjie':
            data['avatar']=item['profile_image']
            data['name']=item['screen_name']
            data['text']=item['text']
            data['image']=item['cdn_img']
            data['width']=item['width']
            data['height']=item['height']
            data['forward']=item['forward']
            data['likes_count'] =int(item['love'])
            data['unlikes_count']=int(item['hate'])
            data['updated_at']=item['create_time']
            data['created_at']=item['create_time']
            data['source_id']=int(item['id'])
        elif channel=='neihan':
            data['avatar']=item['group']['user']['avatar_url']
            data['name']=item['group']['user']['name']
            data['text']=item['group']['content']
            data['image']=item['group']['large_image']['url_list'][0]['url']
            data['width']=item['group']['large_image']['width']
            data['height']=item['group']['large_image']['height']
            data['forward']=item['group']['repin_count']
            data['likes_count'] =item['group']['favorite_count']
            data['unlikes_count']=item['group']['bury_count']
            data['updated_at']=datetime.datetime.fromtimestamp(int(item['online_time'])).strftime('%Y-%m-%d %H:%M:%S')
            data['created_at']=datetime.datetime.fromtimestamp(int(item['online_time'])).strftime('%Y-%m-%d %H:%M:%S')
            data['source_id']=formatId(item['group']['group_id'])
    except:
        return
    return data

def neihan_catch(count):
    params={'category_id':2,
            'level':3,
            'count':30,
            'max_time':1402847474,
            'iid':2209418122,
            'device_id':2665445915,
            'ac':'wifi',
            'channel':'download',
            'aid':7,
            'app_name':'joke_essay',
            'version_code':270,
            'device_platform':'android',
            'device_type':'Galaxy%20S2%20-%204.1.1%20-%20API%2016%20-%20480x800',
            'os_api':16,
            'os_version':'4.1.1',
            'openudid':'9360e54b438cedce'}
    max_time=''
    if not count:
        return
    count=int(count)
    while count:
        url = 'http://ic.snssdk.com/2/essay/zone/category/data/'
        params['max_time']=max_time
        r=requests.get(url,params=params,timeout=5)
        content=r.json()['data']
        dataList=content['data']
        for item in dataList:
            data=parseData(item,'neihan')
            print data
            push2Db(data)
        max_time=content['max_time']
        count-=1


def bdj_catch(count):
    params={
            'a':"newlist",
            'c':"data",
            'page':2,
            'per':20,
            'time':"week",
            'ver':"3.8.3"}
    if not count :
        return
    count=int(count)
    while count:
        url="http://api.budejie.com/api/api_open.php"
        params['page']=count
        response=requests.get(url,params=params,timeout=5)
        content=response.json()
        dataList=content['list']
        print
        print 'length = %d'%len(dataList)
        print
        for item in dataList:
            data=parseData(item,'bdjie')
            push2Db(data)
        count-=1


def main():
    if len(sys.argv)==3:
        app=sys.argv[1]
        count=sys.argv[2]
        if app=='bdjie':
            bdj_catch(count)
        elif app=='neihan':
            neihan_catch(count)
        else:
            print "usage  %s [bdjie|neihan] count "%sys.argv[0]
    else:
        print "usage  %s [bdjie|neihan] count "%sys.argv[0]
        return

if __name__ == '__main__':
    main()
