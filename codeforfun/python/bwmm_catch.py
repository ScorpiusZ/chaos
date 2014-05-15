#! /usr/bin/env python
#ecoding=utf-8
import requests
import md5
import json
import time
import sys


url="http://serverhpapp.kdmobi.com:8888/api/v1/hello.hp"

topic_payload={
        "orderedBy":-1,
        "pageNum":1,
        "pageSize":10,
        "apiCode":"209",
        "appName":"BWMM",
        "systemVersion":"4.3",
        "band":"samsung SCH-I679",
        "secretKey":"414e7251ab25f05b6a65e507010cdf37",
        "sessionToken":"",
        "systemName":"Android",
        "appVersionCode":1997,
        "timestamp":1400038335268}

comment_payload={
        "secretId":150699,
        "pageNum":1,
        "pageSize":10,
        "orderedBy":-1,
        "apiCode":"211",
        "appName":"BWMM",
        "systemVersion":"4.3",
        "band":"samsung SCH-I679",
        "secretKey":"1f1281a840fe7b262d342f232994b628",
        "sessionToken":"",
        "systemName":"Android",
        "appVersionCode":1997,
        "timestamp":1400039026499}

headers={'Content-type':'application/json'
        ,'User-Agent':'android-async-http/1.4.4 (http://loopj.com/android-async-http)' }

current_mili_time=lambda:int(round(time.time()*1000))

def getArticle (sorts,per,page):
    topic_payload["orderedBy"]=sorts
    topic_payload["pageSize"]=per
    topic_payload["pageNum"]=page
    topic_payload['timestamp']=current_mili_time()
    topic_payload['secretKey']=getSecretKey(topic_payload['apiCode'],topic_payload['timestamp'],topic_payload['appVersionCode'])
    r=requests.post(url,data=json.dumps(topic_payload),timeout=5,headers=headers)
    print
    print "getArticle :  page = %d"%(page)
    print
    res=r.json()
    lists=res['secretLists']
    #print lists
    for i in range(len(lists)):
        article=lists[i]
        filename="beiwomm/article/"+"article"+str(article['secretId'])+".json"
        fd=open(filename,'w')
        fd.writelines(json.dumps(article))
        fd.close()
        print
        print article['content']
        print
        getComments(article['secretId'],20,1,int(article['commentNum']))
        break
    return

def getComments (article_id,per,page,count):
    comment_payload["secretId"]=article_id
    comment_payload["pageSize"]=per
    comment_payload["pageNum"]=page
    comment_payload['timestamp']=current_mili_time()
    comment_payload['secretKey']=getSecretKey(comment_payload['apiCode'],comment_payload['timestamp'],comment_payload['appVersionCode'])
    r=requests.post(url,data=json.dumps(comment_payload),timeout=5,headers=headers)
    print "getComments : article_id = %d page = %d count = %d"%(article_id,page,count)
    res=r.json()
    #print res
    lists=res['secretCommentLists']
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

sorts={
       'default':-1,
       'day':1,
       'week':2,
       'month':3,
       'new':4,
       }


def main ():
    if len(sys.argv)>=4:
        category=sys.argv[1]
        if category not in('default','day','week','month','new'):
            print "category should be like default or day or week or month or new"
            return
        else:
            category=sorts[category]
        per=int(sys.argv[2])
        count=int(sys.argv[3])
        print "category=%s per=%d page=%d"%(category,per,count)
    else:
        print "usage:: %s category[default|day|week|month|new] per count "%sys.argv[0]
        print "then this script will download per*count topics"
        print "example bdj_catch.py hot 10 20 will download 200 hot topics"
        return
    page=1
    while page<=count:
        getArticle(category,per,page+1)
        page+=1;

def getSecretKey (apicode,time,appVersionCode):
    seed=str(apicode)+str(appVersionCode)+str(time)+"abcde12345$$%#%##@989KdMobi168"
    byte_seed="".join([elem.encode("utf-8")for elem in seed])
    m=md5.new()
    m.update(byte_seed)
    return m.hexdigest()


if __name__ == '__main__':
    main()
