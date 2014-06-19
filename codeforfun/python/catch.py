#! /usr/bin/env python
#coding:utf8
import requests
import MySQLdb
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
    except:
        return
    return data

def bdj_catch(count):
    if not count :
        return
    count=int(count)
    while count:
        url="http://api.budejie.com/api/api_open.php"
        params={
                'a':"newlist",
                'c':"data",
                'page':2,
                'per':20,
                'time':"week",
                'ver':"3.8.3"}
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
            pass
        else:
            pass
    else:
        print "usage:: %s [bdjie] count "%sys.argv[0]
        return

if __name__ == '__main__':
    main()
