#! /usr/bin/env python
#coding:utf8
import requests
import datetime
import random
from bs4 import BeautifulSoup
import MySQLdb

db=MySQLdb.connect(host='localhost',user='root',passwd='root',port=3306,db='miai',charset='utf8')

def getBirtyDay(age):
    now=datetime.datetime.now().date()
    try:
        birth=datetime.datetime(now.year-age,1,1)
    except:
        return datetime.datetime(1990,1,1)
    return birth

def getEducation(education):
    educations={'初中':1,'高中':2,'中专':2,'大专':3,'本科':4,'硕士':5}
    return getTypeCode(education,educations)

def getMarriage(marriage):
    marriages={'未婚':1,'离异':2,'丧偶':3}
    return getTypeCode(marriage,marriages)

def getProfession(profession):
    professions={'在校学生':1,'军人':5,'私营业主':3,'企业职工':2,'农业劳动者':7,'事业单位工作者':4,'政府机关':4,'自由职业者':6}
    return getTypeCode(profession,professions)

def getBloodType(blood_type):
    bloods={'AB':3,'A':1,'B':2,'O':4}
    return getTypeCode(blood_type,bloods)

def getIsSmoking(smooking):
    smookings={'不抽':2,'偶尔':3,'经常':4,'抽':1}
    return getTypeCode(smooking,smookings)


def getLivingCondition(livingcondition):
    livingconditions={'已购房':1,'与父母同住':2,'租房':3,'其他':4}
    return getTypeCode(livingcondition,livingconditions)

def getIsBeer(isbeer):
    isbeers={'不喝':2,'偶尔':3,'经常':4,'喝':1}
    return getTypeCode(isbeer,isbeers)

def getIsNeedBaby(isneedbaby):
    isneedbabys={'不想':2,'还没想好':3,'想':1}
    return getTypeCode(isneedbaby,isneedbabys)

def getTwoPlacaLove(twoplacelove):
    twoplaceloves={'看情况':2,'不能':3,'能':1}
    return getTypeCode(twoplacelove,twoplaceloves)

def getLiveWithParent(livewithparent):
    livewithparents={'看情况':2,'不愿意':3,'愿意':1}
    return getTypeCode(livewithparent,livewithparents)

def getTypeCode(value,types):
    if not value:
        return 1
    for type_name,type_code in types.items():
        if type_name in value:
            return type_code
    else:
        return random.randint(1,len(types))


def getWeight(weight):
    if '保密' in weight:
        return 120
    else:
        return str(weight).replace('斤','')


def getPhotos(member):
    if not member or not member['photo_list']:
        return []
    else:
        soup=BeautifulSoup(member['photo_list'])
        imgs=soup.findAll('img')
        img_srcs=map(lambda x :x ['src'],imgs)
        return img_srcs

def range_value_of(data,start,end):
    if '-' in data and '不限' not in data:
        return data.split('-')
    else:
        return 0,random.randint(start,end)


def transform_member_to_model(member):
    if not member:
        return None
    elif 'http:' not in member['enlarge_photo'] :
        return None
    else:
        content,basic,avatar,info,detail,monologue,relation_proposal={},{},{},{},{},{},{}
        #basic
        basic['unique_id']=member['id']
        basic['platform']=-1
        #info
        info['height']=member['stature']
        info['birthday']=getBirtyDay(member['age'])
        info['sex']=member['sex']
        info['nickname']=member['nick_name']
        info['location_id']=member['province_id']
        info['weight']=getWeight(member['weight'])
        #avatar
        avatar['avatar']=member['enlarge_photo']
        avatar['status']=0
        #detail
        detail['profession']=getProfession(member['user_raise'])
        detail['education']=getEducation(member['education'])
        detail['salary']=random.randint(1,6)
        detail['marriage']=getMarriage(member['user_marriage'])
        detail['living_condition']=getLivingCondition(member['user_is_house'])
        detail['two_place_love']=getTwoPlacaLove(member['user_is_twoplacelove'])
        detail['live_with_parent']=getLiveWithParent(member['user_livewithparent'])
        detail['smoking']=getIsSmoking(member['user_is_smoking'])
        detail['drinking']=getIsBeer(member['user_is_beer'])
        detail['need_baby']=getIsNeedBaby(member['user_is_needbady'])
        detail['blood_type']=getBloodType(member['user_blood'])
        #monologue
        monologue['title']=member['desc']
        monologue['status']=0
        #relation_proposal
        relation_proposal['location_id']=random.randint(1,30)
        relation_proposal['start_age'],relation_proposal['end_age']=range_value_of(member['user_re_age'],24,50)
        relation_proposal['start_height'],relation_proposal['end_height']=range_value_of(member['user_re_stature'],160,200)
        relation_proposal['lowest_education']=random.randint(1,5)
        relation_proposal['lowest_salary']=random.randint(1,6)
        #photos
        content['photos']=getPhotos(member)
        #tags
        content['charm']=member['user_charm']
        content['character']=member['user_character']
        content['interest']=member['user_interest']
        content['basic'],content['info'],content['detail'],content['monologue'],content['relation_proposal'],content['avatar']=basic,info,detail,monologue,relation_proposal,avatar
        return content


def ExistMember(unique_id):
    cursor=db.cursor()
    sql='select id from members where unique_id = \'{0}\' and platform = -1'.format(unique_id)
    result=cursor.execute(sql)
    if result:
        member_id=cursor.fetchone()[0]
    cursor.close()
    return result if not result else member_id

def insert_member_basic(basic):
    sql='insert into members(unique_id,platform,created_at,updated_at) values(%s,%s,%s,%s)'
    cursor=db.cursor()
    now=datetime.datetime.now()
    result=cursor.execute(sql,[basic['unique_id'],basic['platform'],now,now])
    db.commit()
    cursor.close()

def insert_member_info(info):
    if not info['nickname']:
        info['nickname']= '男士' if info['sex'] == 0 else '女士'
    sql='insert into member_infos(member_id,birthday,sex,nickname,location_id,height,weight,created_at,updated_at) \
            values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    cursor=db.cursor()
    now=datetime.datetime.now()
    result=cursor.execute(sql,[info['member_id'],info['birthday'],info['sex'],info['nickname'],info['location_id'],info['height'],info['weight'],now,now])
    db.commit()
    cursor.close()

def insert_member_avatar(avatar):
    sql='insert into member_avatars(member_id,avatar,status,created_at,updated_at) values(%s,%s,%s,%s,%s)'
    cursor=db.cursor()
    now=datetime.datetime.now()
    result=cursor.execute(sql,[avatar['member_id'],avatar['avatar'],avatar['status'],now,now])
    db.commit()
    cursor.close()

def insert_member_detail(detail):
    sql='insert into member_details(member_id,education,profession,salary,marriage,living_condition,two_place_love,\
            live_with_parent,smoking,drinking,need_baby,blood_type,created_at,updated_at) \
            values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    cursor=db.cursor()
    now=datetime.datetime.now()
    result=cursor.execute(sql,[detail['member_id'],detail['education'],detail['profession'],detail['salary'],\
            detail['marriage'],detail['living_condition'],detail['two_place_love'],detail['live_with_parent'],\
            detail['smoking'],detail['drinking'],detail['need_baby'],detail['blood_type'],now,now])
    db.commit()
    cursor.close()

def insert_member_monologues(monologue):
    sql='insert into member_monologues(member_id,title,status,created_at,updated_at) values(%s,%s,%s,%s,%s)'
    cursor=db.cursor()
    now=datetime.datetime.now()
    result=cursor.execute(sql,[monologue['member_id'],monologue['title'],monologue['status'],now,now])
    db.commit()
    cursor.close()

def insert_member_relation_proposal(relation_proposal):
    sql='insert into member_relation_proposals(member_id,location_id,start_age,end_age,start_height,end_height,lowest_education,lowest_salary,created_at,updated_at)\
            values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    cursor=db.cursor()
    now=datetime.datetime.now()
    result=cursor.execute(sql,[relation_proposal['member_id'],relation_proposal['location_id'],relation_proposal['start_age'],relation_proposal['end_age'],\
            relation_proposal['start_height'],relation_proposal['end_height'],relation_proposal['lowest_education'],relation_proposal['lowest_salary'],now,now])
    db.commit()
    cursor.close()

def insert_member_albums(name,member_id):
    cursor=db.cursor()
    sql='insert into albums(name,member_id,created_at,updated_at) values(%s,%s,%s,%s)'
    now=datetime.datetime.now()
    cursor.execute(sql,[name,member_id,now,now])
    db.commit()
    cursor.close()


def insertMember(member):
    insert_member_basic(member['basic'])
    member_id=ExistMember(member['basic']['unique_id'])
    member['info']['member_id']=member['detail']['member_id']=member['avatar']['member_id']=member['monologue']['member_id']=member['relation_proposal']['member_id']=member_id
    insert_member_info(member['info'])
    insert_member_detail(member['detail'])
    insert_member_avatar(member['avatar'])
    insert_member_monologues(member['monologue'])
    insert_member_relation_proposal(member['relation_proposal'])
    insert_member_albums('photo_list',member_id)
    return member_id


def getTagTypeId(tag_label,tag_type):
    sql='select id from tag_types where name = \'{0}\''.format(tag_type)
    cursor=db.cursor()
    result=cursor.execute(sql)
    if not result:
        sql='insert into tag_types(label,name,created_at,updated_at) values(%s,%s,%s,%s)'
        now=datetime.datetime.now()
        cursor.execute(sql,[tag_label,tag_type,now,now])
        db.commit()
        cursor.close()
        return getTagTypeId(tag_label,tag_type)
    else:
        tag_type_id=cursor.fetchone()[0]
        cursor.close()
        return tag_type_id

def getTagId(tag,tag_type_id):
    sql='select id from tags where name = \'{0}\' and tag_type_id = {1}'.format(tag,tag_type_id)
    cursor=db.cursor()
    result=cursor.execute(sql)
    if not result:
        sql='insert into tags(name,tag_type_id,created_at,updated_at) values(%s,%s,%s,%s)'
        now=datetime.datetime.now()
        cursor.execute(sql,[tag,tag_type_id,now,now])
        db.commit()
        cursor.close()
        return getTagId(tag,tag_type_id)
    else:
        tag_id=cursor.fetchone()[0]
        cursor.close()
        return tag_id

def setMemberTags(member_id,tag_id):
    if not tag_id or not member_id:
        return
    else:
        sql='select member_id from members_tags where member_id = {0} and tag_id ={1}'.format(member_id,tag_id)
        cursor=db.cursor()
        result=cursor.execute(sql)
        if not result:
            sql='insert into members_tags(member_id,tag_id) values(%s,%s)'
            cursor.execute(sql,[member_id,tag_id])
            db.commit()
            cursor.close()


def update_tag(member_id,tag_type,tags):
    if not tags or (len(tags)==1 and '保密' in tags[0]):
        return
    else:
        tag_type_id=getTagTypeId('user_info',tag_type)
        if not tag_type_id:
            return
        for tag in tags:
            tag_id=getTagId(tag,tag_type_id)
            setMemberTags(member_id,tag_id)


def update_tags(member,member_id):
    charms=map(str.strip,member['charm'].split('|'))
    characters=map(str.strip,member['character'].split('|'))
    interests=map(str.strip,member['interest'].split('|'))
    update_tag(member_id,'魅力部位',charms)
    update_tag(member_id,'特点',characters)
    update_tag(member_id,'个人爱好',interests)


def getAlbumsId(name,member_id):
    sql='select id from albums where member_id = {0} and name = \'{1}\''.format(member_id,name)
    cursor=db.cursor()
    result=cursor.execute(sql)
    if not result:
        return getAlbumsId(name,member_id)
    else:
        albums_id=cursor.fetchone()[0]
        cursor.close()
        return albums_id

def update_photos(member,member_id):
    photos=member['photos']
    cursor=db.cursor()
    albums_id=getAlbumsId('photo_list',member_id)
    if not albums_id :
        return
    sql='insert into pictures(album_id,path,created_at,updated_at) values(%s,%s,%s,%s)'
    now=datetime.datetime.now()
    for photo in photos:
        cursor.execute(sql,[albums_id,photo,now,now])
    db.commit()
    cursor.close()

def record_member_info(member):
    if not member:
        return
    try :
        print member['id'],member['enlarge_photo'],member['nick_name'],member['province_id']
    except:
        return
    content=transform_member_to_model(member)
    if not content:
        return
    member_id=ExistMember(content['basic']['unique_id'])
    if not member_id:
        if insertMember(content):
            member_id=ExistMember(content['basic']['unique_id'])
            update_tags(content,member_id)
            update_photos(content,member_id)
            print content['info']['nickname'],content['basic']['unique_id'],'insert success'
        else:
            print content['info']['nickname'],content['basic']['unique_id'],'insert failed'
    else:
        print content['info']['nickname'],content['basic']['unique_id'],' exist'

def get_member_detail(member_id,province_id,work_money,isVip,user_id):
    if not member_id or not province_id:
        return
    url='http://webkitui.youyuan.com/({0})/user_info_ajax_a.jwml?soulcode=&uid={1}&version=40040200&'.format(user_id,member_id)
    response=requests.get(url)
    content=response.content
    if not content:
        return
    else:
        content=eval(content,{'false': False, 'true': True, 'null': None})[0]
        content['province_id']=province_id
        content['isVip']=isVip
        record_member_info(content)


def get_member_list(user_id,sex,province,page):
    if not user_id :
        return
    url='http://webkitui.youyuan.com/({0})/load_adv_search_result_new.jwml?bage=0&city={1}&bstature=0&workmoney=0&sex={2}&cpage={3}'.format(user_id,province,sex,page)
    response=requests.get(url)
    content=response.content
    if content:
        for member in eval(content,{'false': False, 'true': True, 'null': None}):
            member_id,province_id,work_money,isVip=member['userid'],province,member['workMoney'],member['is_vip']
            get_member_detail(member_id,province_id,work_money,isVip,user_id)
    else:
        return

def member_catch():
    #users={'660FB3CA0824B2C0C5D0A718546DE31E267653454':0,'6B1966EAF0CA011E21A49A57E20A486F270622326':1}
    #users={'':0,'6B1966EAF0CA011E21A49A57E20A486F270622326':1}
    users={'660FB3CA0824B2C0C5D0A718546DE31E267653454':0,'':1}
    for user,sex in users.items():
        for province_id in xrange(1,35):
            get_member_list(user,sex,province_id,1)


def main():
    member_catch()

if __name__ == '__main__':
    main()

