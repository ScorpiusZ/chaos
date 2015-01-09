#! /usr/bin/env python
#encoding:utf8
import MySQLdb
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf8')

db=MySQLdb.connect(host='127.0.0.1',user='root',passwd='root',port=3306,db='data_test',charset='utf8')

def getArticleId(title):
    sql_search="select id from articles where title ='{0}' \
            and description ='robot' ".format(title)
    cursor=db.cursor()
    if cursor.execute(sql_search):
        return cursor.fetchone()[0]
    else:
        return 0

def write_a_article(title,tags,content):
    sql_ins='insert into articles(title,body,description,created_at,updated_at) \
                            values(%s,%s,%s,%s,%s)'
    print
    print 'write article  {0} to db'.format(title)
    date_now=datetime.datetime.now()
    cursor=db.cursor()
    cursor.execute(sql_ins,[title,content,'robot',date_now,date_now])
    db.commit()
    article_id=getArticleId(title)
    if article_id:
        print 'article id {1} with title {0} finished'.format(title,article_id)
    else:
        print 'article  with title {0} failed'.format(title)
    print
    cursor.close()
