#! /usr/bin/env python
#coding:utf8
import os
import sys
import api_util
import id_util
from datetime import date,timedelta

LOG_DIR='/Users/ScorpiusZjj/Temp/data/zip'

LIMIT_NUM=15
articles={'ids':{},'device':{}}
products={'ids':{},'device':{}}
orders={'ids':{},'device':{}}
carts={'ids':{},'device':{}}
replies={'ids':{},'device':{}}
topic_creates={'ids':{},'device':{}}
topic_views={'ids':{},'device':{}}
private_msgs={'ids':{},'device':{}}


def countNum(item_id,items,key):
    if item_id in items[key].keys():
        items[key][item_id]=items[key][item_id]+1
    else:
        items[key][item_id]=1

def analyze_item(command,items_dict,get_ids_func):
    print 'analyze_item : command {0}'.format(command)
    pipe=os.popen(command)
    for line in pipe.readlines():
        device_id,item_ids=get_ids_func(line)
        if device_id:
            countNum(device_id,items_dict,'device')
        for item_id in item_ids:
            countNum(item_id,items_dict,'ids')

def generateCommandByPattern(pattern,datetime):
    files='{0}/{1}*'.format(LOG_DIR,datetime)
    return 'zgrep \"{0}\" {1} '.format(pattern,files)

def analyze_articles(datetime):
    pattern='article'
    analyze_item(generateCommandByPattern(pattern,datetime),articles,getIdByApi)

def analyze_products(datetime):
    pattern='GET.*products'
    analyze_item(generateCommandByPattern(pattern,datetime),products,getIdByApi)

def getOnlyDevice(api):
    return str(api).split(' - ')[-1],['test']

def analyze_cart(datetime):
    pattern='POST .*cart'
    analyze_item(generateCommandByPattern(pattern,datetime),carts,getOnlyDevice)

def analyze_reply(datetime):
    pattern='POST .*topics/.*replies'
    analyze_item(generateCommandByPattern(pattern,datetime),replies,getOnlyDevice)

def analyze_topic_create(datetime):
    pattern='POST .*nodes/.*/topics'
    analyze_item(generateCommandByPattern(pattern,datetime),topic_creates,getOnlyDevice)

def analyze_topic_view(datetime):
    pattern='GET .*topics'
    analyze_item(generateCommandByPattern(pattern,datetime),topic_views,getDeviceDetail)

def analyze_private_msg(datetime):
    pattern='POST .*private_messages'
    analyze_item(generateCommandByPattern(pattern,datetime),private_msgs,getOnlyDevice)

def getDeviceDetail(api):
    if '?' in api:
        return '',[]
    else:
        return str(api).split(' - ')[-1],['test']

def getIdByApi(api):
    if '?' in api :
        return '',[]
    else:
        device_id=str(api).split(' - ')[-1]
        url=str(api).split(' - ')[-3]
        return device_id,[str(url).replace("\"","").split('/')[-1]]

def analyze_orders(datetime):
    pattern='string: POST.*orders'
    analyze_item(generateCommandByPattern(pattern,datetime),orders,getOrderProductIds)

def isTestOrder(api):
    for keyword in ('test','测试'):
        if keyword in api:
            return True
    return False

def getOrderProductIds(api):
    order_product_id=[]
    next_contain_product_id=False
    next_contain_device_id=False
    url=api.split(':')[-1]
    device_id=''
    if isTestOrder(api):
        return device_id,[]
    for item in url.split('='):
        if next_contain_product_id :
            order_product_id.append(str(item).replace('product_id','').replace('product_prop_id',''))
        if next_contain_device_id:
            device_id=str(item).replace('name','')
        next_contain_product_id= 'product_id' in item
        next_contain_device_id= 'device_id' in item
    return device_id,order_product_id

def result(item_name,items_dict):
    sorted_items=sorted(items_dict, key=items_dict.get,reverse=True)
    #print 'top {0} items :'.format(LIMIT_NUM)
    #for item in sorted_items[:LIMIT_NUM]:
        #print item_name,item ,items_dict[item]
    #print 'all {1} {0}'.format(len(items_dict),item_name)
    #print
    return sorted_items[:LIMIT_NUM]

def find_products_in_articles(article_ids):
    if not article_ids:
        return
    for article_id in article_ids:
        product_id=api_util.getProductIdInArticle(article_id)
        print 'article id :{0} product id : {1}'.format(article_id,product_id)

def showStatics(article_id,product_id):
    article_sum=articles['ids'][article_id] if article_id in articles['ids'].keys() else 0
    product_sum=products['ids'][product_id] if product_id in products['ids'].keys() else 0
    order_sum=orders['ids'][product_id] if product_id in orders['ids'].keys() else 0
    decrypt_article_id=id_util.decode_article(article_id).strip()
    decrypt_product_id=id_util.decode_product(product_id).strip()
    pattern='article {0:10}:{1:10} ,product {2:10}:{3:10} ,orders {4}'
    print pattern.format(decrypt_article_id,article_sum,decrypt_product_id,product_sum,order_sum)

def test():
    article_1440='b1ddb243fddd5ce061bc24aa60ae7fa6'
    product_4059='a5c78651165fd4845ea1f39698578f63'
    product_4875='69ec4fcb3450ebd81be117f1bd2df0f4'
    article_1441='e6d28c211c56b8e6287f88727835f9e8'
    showStatics(article_1440,product_4059)
    showStatics(article_1441,product_4875)

def analyze_result(datetime):
    for article_id in result('article',articles['ids']):
        product_ids=api_util.getProductIdInArticle(article_id)
        if product_ids:
            for product_id in api_util.getProductIdInArticle(article_id):
                showStatics(article_id,id_util.encode_product(product_id))
        else:
            showStatics(article_id,'')
    showPv()

def getDates(date_from,date_to):
    from_y,from_m,from_d=map(int,date_from.split(','))
    to_y,to_m,to_d=map(int,date_to.split(','))
    d_from=date(from_y,from_m,from_d)
    d_to=date(to_y,to_m,to_d)
    interval=d_to-d_from
    return [d_from+timedelta(days=x) for x in xrange(interval.days+1)]

def clearDict(items):
    for key in items.keys():
        items[key].clear()

def calcPv(name,items):
    view_total=sum(items['ids'].values())
    device_total=len(items['device'].keys())
    print '{2} :view_total {0} : device_total {1}'.format(view_total,device_total,name)

def showPv():
    calcPv('article',articles)
    calcPv('product',products)
    calcPv('order',orders)

def cleardata():
    clearDict(articles)
    clearDict(products)
    clearDict(orders)

def article_category(datetime):
    print 'analyze date :{0}'.format(datetime)
    cleardata()
    analyze_articles(datetime)
    analyze_products(datetime)
    analyze_orders(datetime)
    analyze_result(datetime)

def community_product_result():
    calcPv('products',products)
    calcPv('cart',carts)
    calcPv('reply',replies)
    calcPv('topic_create',topic_creates)
    calcPv('topic_view',topic_views)
    calcPv('private_msg',private_msgs)

def community_product_category(datetime):
    analyze_products(datetime)
    analyze_cart(datetime)
    analyze_reply(datetime)
    analyze_topic_create(datetime)
    analyze_topic_view(datetime)
    analyze_private_msg(datetime)
    community_product_result()

def main():
    for date in getDates('2015,01,05','2015,01,05'):
        community_product_category(str(date).replace('-',''))

if __name__ == '__main__':
    main()
