#! /usr/bin/env python
#coding:utf8
import data_analyze as da
import api_util

def getDataFileName(date,api_key,key):
    import Config
    return '{0}/{1}_{2}{3}'.format(Config.getHomeDateDir(),date,api_key,key)

def md5(content):
    import hashlib
    return hashlib.md5(content).hexdigest()

def saveHomeData(date,api_key,content):
    data_file_name=getDataFileName(date,api_key,md5(content))
    import os
    if os.path.exists(data_file_name):
        return
    else:
        with open(data_file_name,'w') as data_file:
            data_file.write(content)

def getHomeData(date,api_key,registe_date='20140911',version='1.4.1'):
    content=api_util.getHomeData(api_key,registe_date,version)
    saveHomeData(date,api_key,content)

def analyzeItem(item_name,item):
    return item.get('type','') ,item.get('id',''),item.get('title','')

def analyzeItemList(date,item_name,item_list):
    if not item_name == 'sections':
        print
        print item_name
        print
        for item in map(lambda x : analyzeItem(item_name,x),item_list):
            item_type,item_id,item_title=item
            print item_type,item_id,item_title
    else:
        for item in item_list:
            analyzeItemList(date,'sections'+'_'+item['name'],item['objects'])

def analyzeHomeDATA(date,api_key='4def4d59'):
    fileName = getDataFileName(date,api_key)
    with open(fileName,'r') as home_data_file:
        home_data=eval(home_data_file.read(),{'false': False, 'true': True, 'null': None})
        for key in home_data.keys():
            if isinstance(home_data[key],list):
                analyzeItemList(date,key,home_data[key])


def main():
    import datetime,sys
    date=datetime.datetime.now().strftime('%Y%m%d')
    if '-get' in sys.argv:
        getHomeData(date,'4def4d59')
    #analyzeHomeDATA(date)
    #getDataKey(date)

if __name__ == '__main__':
    main()
