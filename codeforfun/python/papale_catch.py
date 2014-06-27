#! /usr/bin/env python
#coding:utf8
import requests
import MySQLdb
import datetime
import sys

db=MySQLdb.connect(host='localhost',user='root',passwd='',port=3306,db='test',charset='utf8')

def Exist(data):
    sql='select * from contents where source_id=%s'%data['source_id']
    cursor=db.cursor()
    count=cursor.execute(sql)
    if count==1:
        return True
    else:
        return False

def push2Db(data):
    if not data:
        return
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
        print '%s ok'%data['source_id']
    except:
        print '%s error'%data['source_id']
        cursor.close()
        return

def formatId(id):
    if id>999999999:
        id=int(id)%1000000000
    return id

def convert_count(count):
    if not count:
        return 0
    else:
        count=int(count)
        return count%50

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
            data['forward']=convert_count(item['forward'])
            data['likes_count'] =convert_count(int(item['love']))
            data['unlikes_count']=convert_count(int(item['hate']))
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
            data['forward']=convert_count(item['group']['repin_count'])
            data['likes_count'] =convert_count(item['group']['favorite_count'])
            data['unlikes_count']=convert_count(item['group']['bury_count'])
            data['updated_at']=datetime.datetime.fromtimestamp(int(item['online_time'])).strftime('%Y-%m-%d %H:%M:%S')
            data['created_at']=datetime.datetime.fromtimestamp(int(item['online_time'])).strftime('%Y-%m-%d %H:%M:%S')
            data['source_id']=formatId(item['group']['group_id'])
        elif channel=='baozou':
            data['avatar']=item['user_avatar']
            data['name']=item['user_login']
            data['text']=item['title']
            data['image']=item['pictures']
            data['width']=item['width']
            data['height']=item['height']
            data['forward']=convert_count(item['reward_count'])
            data['likes_count'] =convert_count(item['pos'])
            unlike=int(item['neg'])
            data['unlikes_count']=convert_count(-unlike)
            data['updated_at']=item['created_at']
            data['created_at']=item['created_at']
            data['source_id']=item['id']
    except:
        return
    return data

def baozou_catch(count,fileter):
    url='http://api.ibaozou.com/groups/1/hottest/%s.app?'
    params={
    'client_id':10230158,
    'ignore_for_mobile':'true',
    'page':1,
    'pagesize':10
    }
    if not count:
        return
    if fileter:
        url=url%fileter
    count=int(count)
    while count:
        params['page']=count
        try:
            response=requests.get(url,params=params,timeout=5)
        except:
            print 'requests timeout'
            continue
        content=response.json()
        dataList=content['articles']
        if not len(dataList):
            break
        for item in dataList:
            data=parseData(item,'baozou')
            push2Db(data)
        count-=1

def neihan_catch(count,fileter):
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
    if fileter:
        params['level']=fileter
    while count:
        url = 'http://ic.snssdk.com/2/essay/zone/category/data/'
        params['max_time']=max_time
        try:
            response=requests.get(url,params=params,timeout=5)
        except:
            print 'requests timeout'
            continue
        content=response.json()['data']
        dataList=content['data']
        if not len(dataList):
            break
        for item in dataList:
            data=parseData(item,'neihan')
            push2Db(data)
        max_time=content['max_time']
        count-=1


def bdj_catch(count,fileter):
    params={
            'a':"newlist",
            'c':"data",
            'page':2,
            'per':20,
            'time':"week",
            'ver':"3.8.3"}
    if not count :
        return
    if fileter:
        params['a']=fileter
    count=int(count)
    while count:
        url="http://api.budejie.com/api/api_open.php"
        params['page']=count
        try:
            response=requests.get(url,params=params,timeout=5)
        except:
            print 'requests timeout'
            continue
        content=response.json()
        dataList=content['list']
        if not len(dataList):
            break
        for item in dataList:
            data=parseData(item,'bdjie')
            push2Db(data)
        count-=1

def dealWithFilter(app,category):
    if app=='bdjie':
        if category not in {'distillate','new'}:
            print'%s\'s category should be like distillate[精华] or new'%app
        else:
            return 'list'if category=='distillate'else 'newlist'
    elif app=='neihan':
        if category not in {'distillate','new','hot','recommand'}:
            print'%s\'s category should be like distillate[精华] or new or hot or recommand'%app
        else:
            fileter={ 'distillate':5, 'new':3,
                    'hot':4,'recommand':6 }
            return fileter[category]
    elif app=='baozou':
        if category not in {'day','week','month','year','8hr'}:
            print'%s\'s category should be like day or week or month or year or 8hr'%app
        else:
            fileter={ 'day':'24hr', 'week':'week',
                    'month':'month','year':'year','8hr':'8hr' }
            return fileter[category]
    else:
        pass

def main():
    if len(sys.argv)==4:
        app=sys.argv[1]
        category=sys.argv[2]
        count=sys.argv[3]
        if app=='bdjie':
            category=dealWithFilter('bdjie',category)
            if category:
                bdj_catch(count,category)
        elif app=='neihan':
            category=dealWithFilter('neihan',category)
            if category:
                neihan_catch(count,category)
        elif app=='baozou':
            category=dealWithFilter('baozou',category)
            if category:
                baozou_catch(count,category)
        else:
            print "usage  %s app[bdjie|neihan|baozou] category[] count "%sys.argv[0]
    else:
        print "usage  %s app[bdjie|neihan|baozou] category count "%sys.argv[0]
        return

if __name__ == '__main__':
    main()
