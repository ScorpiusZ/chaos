#! /usr/bin/env python
#ecoding=utf-8
import requests
import base64
import json
import time
import sys

version="2.7.8"
android_id="IMEI_6fb6cf36b82672d0e1a37e3fea3a3365S"
device_id="IMEI_5284047f4ffb4e04824a2fd1d1f0cd62"
serial="IMEI_d41d8cd98f00b204e9800998ecf8427e"
lang="zh-hans"
sessionid=""
jiankongbao=1
ver="new_version"
secret_token=""
secret_uid=2379206
name="liuxin"

payload={'version':version,
        'android_id':android_id,
        'device_id':device_id,
        'serial':serial,
        'lang':lang,
        'sessionid':sessionid,
        'jiankongbao':jiankongbao,
        'ver':ver,
        'secret_token':secret_token,
        'secret_uid':secret_uid,
        'name':name}

article_url="http://apprequest.secretmimi.com/article"
comments_url="http://apprequest.secretmimi.com/comment/new_comment"

def getTopic_nor ():
    req=urllib2.Request(url)
    print req
    res_data=urllib2.urlopen(req)
    res=res_data.read()
    print res

def getArticle (sorts,per,page):
    Url=article_url+"/"+sorts+"/"+str(per)+"/page/"+str(page)
    try:
        r=requests.get(Url,params=payload,timeout=5)
    except:
        return
    print "getArticle :  page = %d"%(page)
    res=r.json()
    lists=res['list']
    for i in range(len(lists)):
        article=lists[i]
        article['content']=base64.b64decode(article['content'])
        article['title']=base64.b64decode(article['title'])
        article['source_content']=base64.b64decode(article['source_content'])
        filename="mimi/article/"+"article"+str(article['id'])+".json"
        fd=open(filename,'w')
        fd.writelines(json.dumps(article))
        fd.close()
        print article['content']
        getComments(article['id'],20,1,article['public_comments_count'])
    return res['num']

def getComments (article_id,per,page,count):
    Url=comments_url+"/"+str(article_id)+"/list/"+str(per)+"/page/"+str(page)
    try:
        r=requests.get(Url,params=payload,timeout=5)
    except:
        return
    print "getComments : article_id = %d page = %d count = %d"%(article_id,page,count)
    print r.url
    res=r.json()
    lists=res['list']
    filename="mimi/comment"+"/"+str(article_id)+"_comment_"+str(page)+".json"
    fd=open(filename,'w')
    for i in range(len(lists)):
        comment=lists[i]
        comment['content']=base64.b64decode(comment['content'])
        lists[i]=comment
        print comment['content']
    res['list']=lists
    fd.writelines(json.dumps(res))
    fd.close
    time.sleep(1)
    count=count-len(lists)
    print "list size=%d"%len(lists)
    if count<=0 or len(lists)==0:
        print "article : %d is done "%(article_id)
    else:
        page+=1
        getComments(article_id,per,page,count)

sorts={'hot':'hot',
        'week':'week',
        'day':'day',
        'month':'month'}


def main ():
    if len(sys.argv)>=4:
        category=sys.argv[1]
        if category not in('hot','day','week','month'):
            print "category should be like hot or day or week or month "
            return
        else:
            category=sorts[category]
        per=int(sys.argv[2])
        count=int(sys.argv[3])
        print "category=%s per=%d count=%d"%(category,per,count)
    else:
        print "usage:: %s category[hot|day|week|month] per count"%sys.argv[0]
        print "then this script will download per*count topics"
        print "example: mm_catch.py hot 10 20 will download 200 hot topics"
        return
    page=1
    while page<=count:
        getArticle(category,per,page)
        page+=1;

if __name__ == '__main__':
    main()
