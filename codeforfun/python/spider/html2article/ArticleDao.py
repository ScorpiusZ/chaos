#! /usr/bin/env python
#encoding:utf8
import MySQLdb
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf8')

db=MySQLdb.connect(host='127.0.0.1',user='root',passwd='root',port=3306,db='test',charset='utf8')
sql_ins='insert into articles(title,body,created_at,updated_at) \
                    values(%s,%s,%s,%s)'

def write_a_article(title,tags,content):
    print 'write article  {0} to db'.format(title)
    date_now=datetime.datetime.now()
    cursor=db.cursor()
    cursor.execute(sql_ins,[title,content,date_now,date_now])
    db.commit()
    print 'article {0} finished'.format(title)
    cursor.close()
