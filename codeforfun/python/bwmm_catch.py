#! /usr/bin/env python
#ecoding=utf-8
import requests
import urllib2
import json
import time
import sys


url="http://serverhpapp.kdmobi.com:8888/api/v1/hello.hp"

topic_payload={
        "orderedBy":-1,
        "pageNum":1,
        "pageSize":10,
        "apiCode":209,
        "appName":"BWMM",
        "systemVersion":"4.3",
        "band":"samsung SCH-I679",
        "secretKey":"cc54e2f58b3eb6b8c0f8f5ec44262c10",
        "sessionToken":"",
        "systemName":"Android",
        "appVersionCode":"1997",
        "timestamp":"1399974977932",
        }

comment_payload={
        "market":"anzhuo" ,
        "from":"android" ,
        "ver":"2.4.5" ,
        "udid":"000000000000000" ,
        "latlng":"" ,
        "lang":"CN" ,
        "appName":"budejie_mimi" ,
        "mac":"08%3A00%3A27%3A81%3A2d%3A79" ,
        "c":"comment" ,
        "a":"dataList" ,
        "per":20 ,
        "data_id":"103915951" ,
        "page":1 ,
        "userID":"" ,
        "hot":1 }


def getArticle (sorts,per,page):
    #topic_payload["order"]=sorts
    #topic_payload["per"]=per
    #topic_payload["page"]=page
    headers={'Content-type':'application/json','Accept':'text/plain'}
    r=requests.post(url,data=topic_payload,timeout=5,headers=headers)
    print
    print "getArticle :  page = %d"%(page)
    print
    res=r.text
    print res
    #lists=res['list']
    #for i in range(len(lists)):
        #article=lists[i]
        #filename="beiwomm/article/"+"article"+str(article['id'])+".json"
        #fd=open(filename,'w')
        #fd.writelines(json.dumps(article))
        #fd.close()
        #print
        #print article['text']
        #print
        #getComments(article['id'],20,1,int(article['comment']))
    #return

def getComments (article_id,per,page,count):
    comment_payload['data_id']=article_id
    comment_payload['per']=per
    comment_payload['page']=page
    try:
        r=requests.get(url,params=comment_payload,timeout=5)
        print "getComments : article_id = %d page = %d count = %d"%(article_id,page,count)
    except:
        return
    print r.url
    res=r.json()
    lists=res['data']
    if len(lists)==0:
        return
    filename="beiwomm/comment"+"/"+str(article_id)+"_comment_"+str(page)+".json"
    fd=open(filename,'w')
    for i in range(len(lists)):
        comment=lists[i]
        print comment['content']
    fd.writelines(json.dumps(res))
    fd.close
    time.sleep(1)
    count=count-len(lists)
    if count<=1 or len(lists)==0:
        print "article : %d is done "%(article_id)
    else:
        page+=1
        getComments(article_id,per,page,count)

sorts={'hot':'comment',
        'timewarp':'timewarp',
        'normal':''}


def main ():
    if len(sys.argv)>=4:
        category=sys.argv[1]
        if category not in('hot','timewarp','normal'):
            print "category should be like hot or timewarp or normal"
            return
        else:
            category=sorts[category]
        per=int(sys.argv[2])
        count=int(sys.argv[3])
        print "category=%s per=%d page=%d"%(category,per,count)
    else:
        print "usage:: %s category[hot|timewarp|normal] per count "%sys.argv[0]
        print "then this script will download per*count topics"
        print "example bdj_catch.py hot 10 20 will download 200 hot topics"
        return
    page=1
    while page<count:
        getArticle(category,per,page)
        page+=1;


if __name__ == '__main__':
    time={ "1399975086704":"d549f23518f2c58a501a787face1084b",
            "1399975117978":"1592a31a0c1a018e6b0a8f336ddec851",
            "1399975123972":"f9a9a107204247b11a7caa50cba923b1",
            "1399975123975":"2ebcfb18b5e3375b9c1d489df61aafd6"}
    #getArticle('a',1,1)
    for i in time.keys():
        print "time %s code %s md5 %s"%(i,time[i],)
