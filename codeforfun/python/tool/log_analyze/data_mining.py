#! /usr/bin/env python
#coding:utf8
import gzip
import re
import datetime
from urllib import unquote
import Config

LOG_DIR=Config.getLogDir()
CSV_DIR=Config.getCsvDir()

#out_format='time {0:30} ,api {1:12} , AppId {2:10} ,Device_id {3:30} ,values {4}'
out_format='{0},{1},{2},{3},{4}'

def getCsvFile(datetime):
    return '{0}/{1}.csv'.format(CSV_DIR,datetime)

def toCsvFile(content,datetime):
    if content:
        with open(getCsvFile(datetime),'a') as csvFile:
            csvFile.write(content+'\n')

def print_data_mined(time,api,appId,device_id,item_ids):
    return out_format.format(time,api,appId,device_id,':'.join(item_ids))

def getTime(line):
    time=str(line).split('#')[0].replace('I','').replace(',','').replace('[','') if line else ''
    parsed_time=datetime.datetime.strptime(time.strip(),'%Y-%m-%dT%H:%M:%S.%f')
    return parsed_time

def getAppDeviceId(line):
    appId,device_id=str(line).split(' - ')[-2:]
    return appId.strip(),device_id.strip()

def getCartInfos(api):
    order_product_id=[]
    next_contain_product_id=next_contain_device_id=next_contain_appId=False
    device_id=appId=''
    url=api.split(':')[-1]
    if isTestOrder(api):
        return appId,device_id,order_product_id
    for item in url.split('='):
        if next_contain_product_id :
            order_product_id.append(str(item).replace('product_id','').replace('product_prop_id',''))
        if next_contain_device_id:
            device_id=str(item).replace('product_id','')
        if next_contain_appId:
            appId=str(item).replace('device_id','')
        next_contain_product_id= 'product_id' in item
        next_contain_device_id= 'device_id' in item
        next_contain_appId='api_key' in item
    return appId,device_id,order_product_id

def parseCart(line):
    time = getTime(line)
    appId,device_id,product_ids=getCartInfos(line)
    return print_data_mined(time,'cart',appId,device_id,product_ids)

def parseReplies(line):
    appId,device_id=getAppDeviceId(line)
    time =getTime(line)
    topic_id=str(line).split(' - ')[-3].split('/')[-2]
    return print_data_mined(time,'replies',appId,device_id,[topic_id])

def getTargeId(line):
    return '' if '?' in line else str(line).split(' - ')[-3].split('/')[-1].replace('\"','')

def parseArticle(line):
    appId,device_id=getAppDeviceId(line)
    time=getTime(line)
    article_id=getTargeId(line)
    if article_id:
        return print_data_mined(time,'article',appId,device_id,[article_id])

def parseProduct(line):
    appId,device_id=getAppDeviceId(line)
    time=getTime(line)
    product_id=getTargeId(line)
    if product_id:
        return print_data_mined(time,'product',appId,device_id,[product_id])

def parseTopicView(line):
    appId,device_id=getAppDeviceId(line)
    time=getTime(line)
    topic_id=getTargeId(line)
    if topic_id:
        return print_data_mined(time,'topic_view',appId,device_id,[topic_id])

def isTestOrder(api):
    for keyword in ('test','测试'):
        if keyword in api:
            return True
    return False

def getOrderInfos(api):
    order_product_id=[]
    next_contain_product_id=next_contain_device_id=next_contain_appId=False
    device_id=appId=''
    url=api.split(':')[-1]
    if isTestOrder(api):
        return appId,device_id,order_product_id
    for item in url.split('='):
        if next_contain_product_id :
            order_product_id.append(str(item).replace('product_id','').replace('product_prop_id',''))
        if next_contain_device_id:
            device_id=str(item).replace('name','')
        if next_contain_appId:
            appId=str(item).replace('device_id','').replace('comment','').replace('coupon','')
        next_contain_product_id= 'product_id' in item
        next_contain_device_id= 'device_id' in item
        next_contain_appId='api_key' in item
    return appId,device_id,order_product_id

def parseOrder(line):
    time=getTime(line)
    appId,device_id,product_ids=getOrderInfos(line)
    return print_data_mined(time,'orders',appId,device_id,product_ids)

def parseTopicCreate(line):
    appId,device_id=getAppDeviceId(line)
    time=getTime(line)
    node_id=str(line).split(' - ')[-3].split('/')[-2]
    return print_data_mined(time,'topic_create',appId,device_id,[node_id])

def parsePrivateMsg(line):
    appId,device_id=getAppDeviceId(line)
    time=getTime(line)
    return print_data_mined(time,'private_msgs',appId,device_id,[])

def getParamValue(line,key_name):
    api=str(line).split(' - ')[-3].split('?')[-1].replace('\"','')
    for item in api.split('&'):
        if key_name in item:
            return str(item).split('=')[-1]
    else:
        return ''

def parseHome(line):
    appId,device_id=getAppDeviceId(line)
    time=getTime(line)
    registe_date=getRegisteDate(line,'registe_date')
    return print_data_mined(time,'home',appId,device_id,[registe_date] if registe_date else [])

def parseProductList(line):
    appId,device_id=getAppDeviceId(line)
    time=getTime(line)
    tag_name=unquote(getParamValue(line,'tag'))
    return print_data_mined(time,'product_list',appId,device_id,[tag_name] if tag_name else [])

def parseCategories():
    return {
            'GET .*home?':parseHome,
            'GET .*products?':parseProductList,
            'string: POST.*cart':parseCart,
            'GET .*articles/':parseArticle,
            'GET .*products/':parseProduct,
            'GET .*topics/':parseTopicView,
            'string: POST.*orders':parseOrder,
            'POST .*nodes/.*/topics':parseTopicCreate,
            'POST .*private_messages':parsePrivateMsg,
            'POST .*topics/.*replies':parseReplies,
            }

def parseData(line,datetime):
    for pattern,parseFunc in parseCategories().items():
        if re.search(pattern,line):
            toCsvFile(parseFunc(line),datetime)

def readFromGzipFile(filename,func_parse_data,datetime):
    with gzip.open(filename,'r') as gzfile:
        for line in gzfile:
            func_parse_data(line,datetime)

def getData(datetime):
    for no in [1,2,3]:
        gzfile='{0}/{1}.log{2}.gz'.format(LOG_DIR,datetime,no)
        readFromGzipFile(gzfile,parseData,datetime)


def main():
    getData('20150105')

if __name__ == '__main__':
    main()
