#! /usr/bin/env python
#coding:utf8
import os
import api_util

LOG_DIR='/Users/ScorpiusZjj/Temp/data/zip'

LIMIT_NUM=15
articles={}
products={}
orders={}

def countNum(item_id,items):
    if item_id in items.keys():
        items[item_id]=items[item_id]+1
    else:
        items[item_id]=1

def analyze_item(command,items_dict,get_ids_func,seprator,pos):
    print 'analyze_item : command {0}'.format(command)
    pipe=os.popen(command)
    for line in pipe.readlines():
        api = line.split(seprator)[-pos]
        item_ids=get_ids_func(api)
        for item_id in item_ids:
            countNum(item_id,items_dict)

def generateCommandByPattern(pattern,datetime):
    files='{0}/{1}*'.format(LOG_DIR,datetime)
    return 'zgrep \"{0}\" {1} '.format(pattern,files)

def analyze_articles(datetime):
    pattern='article'
    analyze_item(generateCommandByPattern(pattern,datetime),articles,getIdByApi,' - ',3)

def analyze_products(datetime):
    pattern='GET.*products'
    analyze_item(generateCommandByPattern(pattern,datetime),products,getIdByApi,' - ',3)

def getIdByApi(api):
    if '?' in api :
        return []
    else:
        return [str(api).replace("\"","").split('/')[-1]]

def analyze_orders(datetime):
    pattern='string: POST.*orders'
    analyze_item(generateCommandByPattern(pattern,datetime),orders,getOrderProductIds,':',1)

def getOrderProductIds(api):
    order_product_id=[]
    next_contain_product_id=False
    for item in api.split('='):
        if next_contain_product_id :
            order_product_id.append(str(item).replace('product_id','').replace('product_prop_id',''))
        if 'product_id' in item:
            next_contain_product_id=True
        else:
            next_contain_product_id=False
    return order_product_id

def result(item_name,items_dict):
    sorted_items=sorted(items_dict, key=items_dict.get,reverse=True)
    print 'top {0} items :'.format(LIMIT_NUM)
    for item in sorted_items[:LIMIT_NUM]:
        print item_name,item ,items_dict[item]
    print 'all {1} {0}'.format(len(items_dict),item_name)
    print
    return sorted_items[:LIMIT_NUM]

def find_products_in_articles(article_ids):
    if not article_ids:
        return
    for article_id in article_ids:
        product_id=api_util.getProductIdInArticle(article_id)
        print 'article id :{0} product id : {1}'.format(article_id,product_id)

def showStatics(article_id,product_id):
    article_sum=articles[article_id] if article_id in articles.keys() else 0
    product_sum=products[product_id] if product_id in products.keys() else 0
    order_sum=orders[product_id] if product_id in orders.keys() else 0
    print 'article : {0}  , product :{1} ,orders :{2}'.format(article_sum,product_sum,order_sum)

def test():
    article_1440='b1ddb243fddd5ce061bc24aa60ae7fa6'
    product_4059='e0314a96abcb9fd263347e3c8fa91b6b'
    product_4875='56e616935976d621ea4031f0be98b07b'
    article_1441='e6d28c211c56b8e6287f88727835f9e8'
    showStatics(article_1440,product_4059)
    showStatics(article_1441,product_4875)


def main():
    date='20150105'
    analyze_articles(date)
    find_products_in_articles(result('article',articles))
    #analyze_products(date)
    #result('product',products)
    #analyze_orders(date)
    #result('order_product_id',orders)

if __name__ == '__main__':
    main()
