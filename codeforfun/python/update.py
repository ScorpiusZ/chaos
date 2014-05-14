#! /usr/bin/env python
#ecoding=utf-8
import glob
import os
import sys
import MySQLdb
import datetime
from random import randrange

Dir_articles='mimi/article/*.json'
Dir_comments='mimi/comment/'

Dir_articles_bd='bdjie/article/*.json'
Dir_comments_bd='bdjie/comment/'

Dir_articles_bwmm='beiwomm/article/*.json'
Dir_comments_bwmm='beiwomm/comment/'

countswitch=True
count=200
node_id=4

sql_ar_find="select id from topics where device_id="

sql_ar_ins_bd="insert into\
               topics(device_id,node_id,body,nickname,\
               likes_count,unlikes_count,created_at,updated_at,member_id) \
               values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"

sql_ar_ins="insert into \
            topics(device_id,node_id,body,nickname,\
            likes_count,unlikes_count,created_at,updated_at,title,member_id) \
            values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

sql_co_ins="insert into\
            replies(body,topic_id,nickname,\
            created_at,updated_at,replyable_type,replyable_id,member_id) \
            values(%s,%s,%s,%s,%s,%s,%s,%s)"


#db=MySQLdb.connect(host='172.16.1.59',user='zjj',passwd='zjj',port=3306,db='adult_things_dev',charset='utf8')
db=MySQLdb.connect(host='localhost',user='root',passwd='',port=3306,db='adult_shop',charset='utf8')

def update_mimi():
    flist=glob.glob(Dir_articles)
    i=1
    print "sum = %d"%(len(flist))
    for jsonfile in flist:
        print jsonfile
        f=file(str(jsonfile))
        content=f.read()
        try:
            content=eval(content,{'false': False, 'true': True, 'null': None})
        except:
            print "convert to dict error"
            continue
        article_id=content['id']
        #do not insert same topics
        if TopicExist(article_id):
            continue
        else:
            topic_id=mimi_topic_ins(content)
        if topic_id==0:
            continue
        else:
            i+=1
            update_mimi_comments(topic_id,article_id)
            update_replycount(topic_id)
        if countswitch and i==count:
            print
            print "count = %d"%(i)
            break

def update_dbj():
    flist=glob.glob(Dir_articles_bd)
    i=1
    print "sum = %d"%(len(flist))
    for jsonfile in flist:
        print jsonfile
        f=file(str(jsonfile))
        content=f.read()
        try:
            content=eval(content,{'false': False, 'true': True, 'null': None})
        except:
            print "convert to dict error"
            return
        article_id=content['id']
        #do not insert same topics
        if TopicExist(article_id):
            continue
        else:
            topic_id=bdj_topic_ins(content)
        if topic_id==0:
            print "insert article_id:%d error"%article_id
            continue
        else:
            i+=1
            update_bdj_comments(topic_id,article_id)
            update_replycount(topic_id)
        if countswitch and i==count:
            print
            print "count = %d"%(i)
            break

def update_bwmm():
    flist=glob.glob(Dir_articles_bwmm)
    i=1
    print "sum = %d"%(len(flist))
    for jsonfile in flist:
        print jsonfile
        f=file(str(jsonfile))
        content=f.read()
        try:
            content=eval(content,{'false': False, 'true': True, 'null': None})
        except:
            print "convert to dict error"
            return
        article_id=content['secretId']
        topic_id=0
        if TopicExist(article_id):
            continue
        else:
            topic_id=bwmm_topic_ins(content)
        if topic_id==0:
            print "insert article_id:%d error"%article_id
            continue
        else:
            i+=1
            update_bwmm_comments(topic_id,article_id)
            update_replycount(topic_id)
        if countswitch and i==count:
            print
            print "count = %d"%(i)
            break


def update_bwmm_comments (topic_id,article_id):
    files=Dir_comments_bwmm+str(article_id)+'_comment_*.json'
    print "comments files :%s"%files
    flist=glob.glob(files)
    for jsonfile in flist:
        f=file(str(jsonfile))
        content=f.read()
        try:
            content=eval(content,{'false': False, 'true': True, 'null': None})
        except:
            print "convert to dict error"
            return
        replies=content['secretCommentLists']
        for i in range(len(replies)):
            reply=replies[i]
            print "comments : %s  num: %d"%(jsonfile,i)
            if reply:
                bwmm_replies_ins(topic_id,reply)
            else:
                print "%s is null"%jsonfile
                break


def update_bdj_comments (topic_id,article_id):
    files=Dir_comments_bd+str(article_id)+'_comment_*.json'
    print "comments files :%s"%files
    flist=glob.glob(files)
    for jsonfile in flist:
        f=file(str(jsonfile))
        content=f.read()
        try:
            content=eval(content,{'false': False, 'true': True, 'null': None})
        except:
            print "convert to dict error"
            return
        replies=content['data']
        for i in range(len(replies)):
            reply=replies[i]
            print "comments : %s  num: %d"%(jsonfile,i)
            if reply:
                bdj_replies_ins(topic_id,reply)
            else:
                print "%s is null"%jsonfile
                break

def update_mimi_comments(topic_id,article_id):
    files=Dir_comments+str(article_id)+'_comment_*.json'
    print "comments files :%s"%files
    flist=glob.glob(files)
    for jsonfile in flist:
        f=file(str(jsonfile))
        content=f.read()
        try:
            content=eval(content,{'false': False, 'true': True, 'null': None})
        except:
            print "convert to dict error"
            return
        replies=content['list']
        for i in range(len(replies)):
            reply=replies[i]
            print "comments : %s  num: %d"%(jsonfile,i)
            if reply:
                mimi_replies_ins(topic_id,reply)
            else:
                print "%s is null"%jsonfile
                break

#db operation
def mimi_topic_ins (topics):
    cursor=db.cursor()
    member_id=0
    try:
        device_id='simulator'+str(topics['id'])
        title=topics['title'].decode('unicode_escape')
        body=topics['content'].decode('unicode_escape')
        nickname=topics['login'].decode('unicode_escape')
        likes_count=topics['hug_num']
        time=topics['post_at']
        time=datetime.datetime.fromtimestamp(int(time)).strftime('%Y-%m-%d %H:%M:%S')
        unlikes_count=topics['attention_num']
        gender=topics['gender']
        member_id=getMemberId(nickname,gender)
        if member_id != 0:
            cursor.execute(sql_ar_ins,[device_id,node_id,body,nickname,likes_count,unlikes_count,time,time,title,member_id])
        else:
            return 0
    except:
        cursor.close()
        return 0
    db.commit()
    sql1=sql_ar_find+"'"+device_id+"'"
    print sql1
    count=cursor.execute(sql1)
    ar_id=0
    if count==1:
        ar=cursor.fetchone()
        ar_id=ar[0]
    db.commit()
    cursor.close()
    return ar_id

def mimi_replies_ins(topic_id,reply):
    cursor=db.cursor()
    member_id=0
    try:
        body=reply['content'].decode('unicode_escape')
        nickname=reply['login'].decode('unicode_escape')
        time=reply['created_at']
        time=datetime.datetime.fromtimestamp(int(time)).strftime('%Y-%m-%d %H:%M:%S')
        gender=reply['gender']
        member_id=getMemberId(nickname,gender)
        if member_id != 0:
            cursor.execute(sql_co_ins,[body,topic_id,nickname,time,time,'Topic',topic_id,member_id])
        else:
            return
    except:
        db.commit()
        cursor.close()
        return
    db.commit()
    cursor.close()

def bdj_replies_ins (topic_id,reply):
    cursor=db.cursor()
    member_id=0
    try:
        body=reply['content'].decode('unicode_escape')
        nickname=reply['user']['username'].decode('unicode_escape')
        time=reply['ctime']
        gender=0 if reply['user']['sex']=='f' else 1
        member_id=getMemberId(nickname,gender)
        if member_id != 0:
            cursor.execute(sql_co_ins,[body,topic_id,nickname,time,time,'Topic',topic_id,member_id])
        else:
            return
    except:
        db.commit()
        cursor.close()
        return
    db.commit()
    cursor.close()

def bwmm_replies_ins (topic_id,reply):
    cursor=db.cursor()
    member_id=0
    try:
        body=reply['content'].decode('unicode_escape')
        nickname=reply['userName'].decode('unicode_escape')
        time=reply['commentTime']
        gender=randrange(0,2)%2
        member_id=getMemberId(nickname,gender)
        if member_id != 0:
            cursor.execute(sql_co_ins,[body,topic_id,nickname,time,time,'Topic',topic_id,member_id])
        else:
            return
    except:
        db.commit()
        cursor.close()
        return
    db.commit()
    cursor.close()

def bdj_topic_ins (topics):
    cursor=db.cursor()
    member_id=0
    try:
        device_id='simulator'+str(topics['id'])
        body=topics['text'].decode('unicode_escape')
        nickname=topics['username'].decode('unicode_escape')
        likes_count=int(topics['love'])
        time=topics['created_at']
        unlikes_count=int(topics['hate'])
        gender=0 if topics['sex']=='f' else 1
        member_id=getMemberId(nickname,gender)
        if member_id != 0:
            cursor.execute(sql_ar_ins_bd,[device_id,node_id,body,nickname,likes_count,unlikes_count,time,time,member_id])
        else:
            return 0
    except:
        cursor.close()
        return 0
    db.commit()
    sql1=sql_ar_find+"'"+device_id+"'"
    print sql1
    count=cursor.execute(sql1)
    ar_id=0
    if count==1:
        ar=cursor.fetchone()
        ar_id=ar[0]
    db.commit()
    cursor.close()
    return ar_id

def bwmm_topic_ins (topics):
    cursor=db.cursor()
    member_id=0
    try:
        device_id='simulator'+str(topics['secretId'])
        body=topics['content'].decode('unicode_escape')
        nickname=topics['authorDisplayName'].decode('unicode_escape')
        likes_count=int(topics['likeNum'])
        time=topics['createdAt']
        unlikes_count=int(topics['unlikeNum'])
        gender=0 if topics['gender']==1 else 1
        member_id=getMemberId(nickname,gender)
        if member_id != 0:
            cursor.execute(sql_ar_ins_bd,[device_id,node_id,body,nickname,likes_count,unlikes_count,time,time,member_id])
        else:
            return 0
    except:
        cursor.close()
        return 0
    db.commit()
    sql1=sql_ar_find+"'"+device_id+"'"
    print sql1
    count=cursor.execute(sql1)
    ar_id=0
    if count==1:
        ar=cursor.fetchone()
        ar_id=ar[0]
    db.commit()
    cursor.close()
    return ar_id


def getAvatar (num):
    url='http://image.yepcolor.com/v2/public-avatars/'
    num=int(num)
    num=getAvatarNum(num)
    url=url+str(num)
    url=url+".png"
    return url

def getAvatarNum (num):
    if not num:
        return 1
    size=74
    num=num%74
    if num<10:
        return '00'+str(num)
    elif num <100:
        return '0'+str(num)
    else:
        return str(num)

def getMemberId (nickname,gender):
    sql_mem_find="select id from members where nickname="
    sql_mem_ins='insert into members(nickname,gender,avatar,created_at,updated_at,robot) \
                            values(%s,%s,%s,%s,%s,%s)'
    avatar=getAvatar(randrange(0,10000))
    if gender!=1 and gender!=0:
        gender=1
    cursor=db.cursor()
    nickname=str(nickname)
    now=datetime.datetime.now()
    sql_mem_find=sql_mem_find+"\""+nickname+"\""
    try:
        count=cursor.execute(sql_mem_find)
    except:
        cursor.close()
        return
    if count==0:
        try:
            cursor.execute(sql_mem_ins,[nickname,gender,avatar,now,now,1])
            db.commit()
            count=cursor.execute(sql_mem_find)
        except:
            cursor.close()
            return 0
        if count==1:
            result=cursor.fetchone()
            return result[0]
    else:
        result=cursor.fetchone()
        return result[0]


def update_replycount (topic_id):
    count=getReplyCount(topic_id)
    sql='update topics set replies_count=%d where id=%d'%(count,topic_id)
    cursor=db.cursor()
    if count!=0:
        cursor.execute(sql)
        db.commit()

def getReplyCount (topic_id):
    sql='select count(*) from replies where topic_id='+str(topic_id)
    cursor=db.cursor()
    count=cursor.execute(sql)
    result=cursor.fetchone()
    return result[0]

def TopicExist (topic_id):
    cursor=db.cursor()
    topic_id='simulator'+str(topic_id)
    sql="select * from topics where device_id ='%s'"%str(topic_id)
    count=cursor.execute(sql)
    if count==1:
        return True
    else:
        return False

def deleteWrongDate ():
    topic_ids=getWrongTopic()
    for item in topic_ids:
        deleteWrongTopic(item[0])
    deleteNullMemberRepliy()


def deleteNullMemberRepliy ():
    cursor=db.cursor()
    sql='delete from replies where member_id is null and device_id is null'
    cursor.execute(sql)
    db.commit()
    cursor.close()

def deleteWrongTopic (topic_id):
    deleteWrongReplies(topic_id)
    sql='delete from topics where id=%d'%topic_id
    cursor=db.cursor()
    cursor.execute(sql)
    db.commit()
    cursor.close()

def deleteWrongReplies (topic_id):
    cursor=db.cursor()
    sql='delete from replies where topic_id=%d'%topic_id
    cursor.execute(sql)
    cursor.close()
    db.commit()

def getWrongTopic ():
    sql='select id from topics where node_id=4 and member_id is null '
    cursor=db.cursor()
    cursor.execute(sql)
    return cursor.fetchall()

def DateAddDays (time,days):
    time=datetime.datetime.strptime(time,'%Y-%m-%d %H:%M:%S')
    date=time+datetime.timedelta(days=days)
    return date

def main ():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    update_mimi()
    print
    print "mimi is done "
    print
    update_dbj()
    print
    print "bd is done "
    print
    update_bwmm()
    print
    print "bwmm is done "
    print
    deleteWrongDate()
    db.close()



if __name__ == '__main__':
    main()
