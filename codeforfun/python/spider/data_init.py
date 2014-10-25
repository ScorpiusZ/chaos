#! /usr/bin/env python
#coding:utf8
import requests
from bs4 import BeautifulSoup
import urllib
import sys
import datetime
import MySQLdb
from random import randrange

reload(sys)
sys.setdefaultencoding('utf-8')

db=MySQLdb.connect(host='localhost',user='root',passwd='',port=3306,db='adult_shop',charset='utf8')

def getHtmlContent(url):
    return requests.get(url,timeout=10).content

def qwys_get():
    for page in xrange(1,3):
        qwys_get_list(page)

def qwys_get_list(page):
    url='http://www.qiwenmi.com/qwys/{0}.html'
    url_root='http://www.qiwenmi.com{0}'
    html=getHtmlContent(url.format(page))
    soup=BeautifulSoup(html)
    page_lb=soup.findAll('div',class_='page_lb')
    divs=soup.findAll('div',class_='sublist')
    for div in divs:
        detail_url=url_root.format(div.h3.find('a').get('href'))
        qwys_detail_get(detail_url,url_root)


def qwys_detail_get(url,url_root):
    html=getHtmlContent(url)
    soup=BeautifulSoup(html)
    content_div=soup.find('div',class_='content')
    title=content_div.find('div',class_='content_tit')
    topic=getTopicTemplate()
    topic['title']=title.text
    images=content_div.find('div',class_='content_pic small')
    #print images
    for link in images.findAll('a'):
        image_url=url_root.format(link.find('img').get('src'))
        topic['imgs'].append(image_url)
    content_p=''
    for p in images.findAll('p'):
        content_p+=p.text
    topic['node_id']=10
    topic['nickname']='首趣'
    topic['body']=content_p
    print topic
    pushTopic2Db(topic,1)


def bmxz_get():
    for page in xrange(1,2):
        bmxz_get_list(page)

def bmxz_get_list(page):
    url='http://www.puahome.com/bbs/f-101-{0}.html'.format(page)
    url_root='http://www.puahome.com/bbs{0}'
    headers={
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36',
        'Cookie':' kvmi_2132_saltkey=J0AijZjR; kvmi_2132_lastvisit=1413789704; kvmi_2132_visitedfid=101; YJS=fe8e1ff0f4ea673fc5918d39b77b5142,MTQxMzc5NjkwNQ==; _gat=1; kvmi_2132_st_t=0%7C1413793522%7Caf83356ab50c15181ced25a705a58cc3; kvmi_2132_forum_lastvisit=D_101_1413793522; kvmi_2132_sid=gklFjZ; Hm_lvt_9f611a57eb6ed694c8e96cb075ecc0f6=1413793306; Hm_lpvt_9f611a57eb6ed694c8e96cb075ecc0f6=1413793524; _ga=GA1.2.1011294069.1413793306; kvmi_2132_lastact=1413793523%09connect.php%09check'
            }
    html=requests.get(url,headers=headers,timeout=10).content
    soup=BeautifulSoup(html)
    tag_ul=soup.find('ul',class_='plist')
    for li in tag_ul.findAll('li'):
        detail_url=url_root.format(li.find('a').get('href'))
        bmxz_get_detail(detail_url,url_root)
        break

def bmxz_get_detail(url,url_root):
    headers={
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36',
        'Referer':'http://www.puahome.com/bbs/f-101-1.html',
        'Cookie':'kvmi_2132_saltkey=J0AijZjR; kvmi_2132_lastvisit=1413789704; kvmi_2132_visitedfid=101; YJS=fe8e1ff0f4ea673fc5918d39b77b5142,MTQxMzc5NjkwNQ==; kvmi_2132_st_t=0%7C1413794002%7Cd08c33bada70d9d6509d646b8b9b8b11; kvmi_2132_forum_lastvisit=D_101_1413794002; kvmi_2132_st_p=0%7C1413795150%7C2e9b32ccd1ad9ddb2027523d485fffa7; kvmi_2132_viewid=tid_66892; kvmi_2132_sid=v6pcp6; Hm_lvt_9f611a57eb6ed694c8e96cb075ecc0f6=1413793306; Hm_lpvt_9f611a57eb6ed694c8e96cb075ecc0f6=1413795152; _ga=GA1.2.1011294069.1413793306; kvmi_2132_lastact=1413795151%09connect.php%09check'
            }
    html=requests.get(url,headers=headers,timeout=10).content
    soup=BeautifulSoup(html)
    print html
    content_tab=soup.find('table',class_='plhin')
    print content_tab

def gms_get(count):
    url='http://www.520guimi.com/mobi/v6/stream/threads_list.json'
    data='track={0}&fid=107&channel=1002005&client_version_code=10901&deviceId=A000004800AE17&auth=&pauth='
    img_root='http://s.guimi.vanchu.com/{0}'
    track=''
    headers={
        'content-type':'application/x-www-form-urlencoded',
            }
    i=0
    while i<count:
        response=requests.post(url,headers=headers,data=data.format(track),timeout=10)
        content=eval(response.text)
        track=content['track']
        dataList=content['data']
        for item in dataList:
            topic=getTopicTemplate()
            topic['node_id']=8
            keys=item.keys()
            if 'author' in keys:
                topic['nickname']=item['author']['nickname'].decode('unicode_escape')
                i=i+1
            else:
                continue
            topic['body']=item['content'].decode('unicode_escape')
            if 'imgGroups' in keys:
                topic['imgs']=[]
                for img in item['imgGroups']:
                    topic['imgs'].append(img_root.format(img))
            print topic
            pushTopic2Db(topic,0)


def nrq_get(count_page):
    url='http://mapi.mama.cn/womanquan/v1_0_0/api/mamaquan/mmq_thread_list.php'
    params={
            'dateline':'',
            'device_id':'A000004800AE17',
            'digest':0,
            'fid':7,
            'page':1,
            'perpage':20,
            'source':1,
            't':1414205207,
            'top':0,
            'type':1,
            'uid':'',
            'token':'94035f5729ec95fd4e14cbdf852f1b07'
            }
    page=1
    while page<count_page:
        params['page']=page
        response=requests.get(url,params=params,timeout=10)
        page=page+1
        content = eval(response.content,{'false': False, 'true': True, 'null': None})
        dataList=content['data']
        for item in dataList:
            print item['author']
            print item['subject']

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
            topic=getTopicTemplate()
            topic['node_id']=6
            if 'group' not in item.keys():
                return
            topic['nickname']=item['group']['user']['name']
            topic['body']=item['group']['content']
            topic['imgs']=[item['group']['large_image']['url_list'][0]['url']]
            pushTopic2Db(topic,1)
        max_time=content['max_time']
        count-=1

def bdj_catch(count,fileter):
    params={
            'a':"list",
            'c':"data",
            'page':1,
            'per':20,
            'time':"week",
            'ver':"3.9.4"}
    if not count :
        return
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
            topic=getTopicTemplate()
            topic['nickname']=item['name']
            topic['body']=item['text']
            topic['imgs']=[item['cdn_img']]
            topic['node_id']=9
            print topic
            pushTopic2Db(topic,1)
        count-=1

def bdj_get(count):
    bdj_catch(count,'new')

def neihan_get(count):
    neihan_catch(count,'hot')

def getMemberId (nickname,gender):
    sql_mem_find="select id from members where nickname='{0}'"
    sql_mem_ins='insert into members(nickname,gender,avatar,created_at,updated_at,robot) \
                            values(%s,%s,%s,%s,%s,%s)'
    avatar=getAvatar(gender)
    if gender!=1 and gender!=0:
        gender=1
    cursor=db.cursor()
    now=datetime.datetime.now()
    sql_mem_find=sql_mem_find.format(nickname)
    #print 'getMemberId :: sql ',sql_mem_find
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

def getAvatar (gender):
    base_url='http://image.yepcolor.com/v2/public-avatars/'
    if gender==1:
        url=base_url+avatar_male[randrange(0,len(avatar_male))]
    elif gender==0:
        url=base_url+avatar_female[randrange(0,len(avatar_female))]
    else:
        url=base_url+avatar_unknow[randrange(0,len(avatar_unknow))]
    return url

avatar_male=( '003.png', '004.png', '006.png', '008.png',
              '009.png', '010.png', '011.png', '012.png',
              '013.png', '022.png', '023.png', '026.png',
              '031.png', '032.png', '033.png', '034.png',
              '035.png', '038.png', '039.png', '041.png',
              '046.png', '049.png', '052.png', '055.png',
              '056.png', '057.png', '058.png', '062.png',
              '063.png', '064.png', '070.png', '071.png',
              '072.png', )

avatar_female=( '007.png', '014.png', '015.png', '016.png',
                '017.png', '018.png', '019.png', '020.png',
                '021.png', '024.png', '025.png', '027.png',
                '037.png', '042.png', '043.png', '044.png',
                '047.png', '048.png', '050.png', '051.png',
                '059.png', '060.png', '061.png', '066.png',
                '068.png', '069.png', '073.png', )

avatar_unknow=( '000.png', '001.png', '002.png', '005.png',
                '028.png', '029.png', '030.png', '036.png',
                '040.png', '045.png', '053.png', '054.png',
                '065.png', '067.png', )


def pushTopic2Db(topic,gender):
    ins_topic="insert into\
               topics(device_id,node_id,title,body,nickname,\
               created_at,updated_at,member_id) \
               values(%s,%s,%s,%s,%s,%s,%s,%s)"
    member_id=getMemberId(topic['nickname'],gender)
    if not member_id:
        print 'no member found '
        return
    else:
        print 'pushTopic2Db :: member_id',member_id
        topic['member_id']=member_id
        topic_id=getTopicIdFromDb(topic)
        if topic_id>0:
            print 'has topic_id',topic_id
            return
        cursor=db.cursor()
        try:
            if 'title' in topic.keys():
                cursor.execute(ins_topic,\
                        [topic['device_id'],topic['node_id'],topic['title'],topic['body'],topic['nickname']\
                            ,topic['created_at'],topic['updated_at'],topic['member_id']])
            else:
                cursor.execute(ins_topic,\
                        [topic['device_id'],topic['node_id'],topic['body'],topic['body'],topic['nickname']\
                            ,topic['created_at'],topic['updated_at'],topic['member_id']])
        except:
            print 'failed '
            return
        db.commit()
        if 'imgs' in topic.keys():
            topic_id=getTopicIdFromDb(topic)
            print 'has imgs topic_id : {0}'.format(topic_id)
            if topic_id>0:
                for img in topic['imgs']:
                    pushTopicImage2Db(topic_id,img)
        cursor.close

def getTopicIdFromDb(topic):
    sql="select id from topics where member_id={0} and body='{1}'".format(topic['member_id'],topic['body'])
    cursor=db.cursor()
    #print 'getTopicIdFromDb sql :',sql
    try:
        count=cursor.execute(sql)
        print count
        if count==1:
            result=cursor.fetchone()
            return result[0]
        else:
            return 0
    except:
        return 0

def pushTopicImage2Db(topic_id,img):
    print 'pushTopicImage2Db topic_id: {0}  img :{1}'.format(topic_id,img)
    now=datetime.datetime.now()
    ins_topic_img='insert into \
            topic_images(topic_id,image,created_at,updated_at) \
            values(%s,%s,%s,%s)'
    cursor=db.cursor()
    cursor.execute(ins_topic_img,[topic_id,img,now,now])
    db.commit()
    cursor.close()

def getTopicTemplate():
    now=datetime.datetime.now()
    topic={}
    topic['imgs']=[]
    topic['device_id']='spiderblsm'
    topic['created_at']=now
    topic['updated_at']=now
    return topic

def dbtest():
    now=datetime.datetime.now()
    topic={}
    body='body{0}'
    nickname='nickname{0}'
    topic['device_id']='1122334455'
    topic['node_id']='1'
    topic['created_at']=now
    topic['updated_at']=now
    for i in xrange(10):
        topic['body']=body.format(i)
        topic['nickname']=nickname.format(i)
        pushTopic2Db(topic,1)

def main():
    #qwys_get()
    #bmxz_get()
    #gms_get(30)
    #nrq_get(3)
    #dbtest()
    #bdj_get(1)
    neihan_get(1)

if __name__ == '__main__':
    main()
