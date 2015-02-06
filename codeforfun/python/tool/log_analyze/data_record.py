#! /usr/bin/env python
#coding:utf8
import data_analyze as da
import id_util as idu
import configs.db as db

def product_record(date):
    global products
    for product_id in products.keys():
        pv=products.get(product_id,0)
        product_id=idu.decode_product(product_id)
        if not db.update_product(product_id,pv,date):
            db.update_product(product_id,pv,date)
            print product_id,pv,date,'retry'
        else:
            print product_id,pv,date,'success'

def product_list_record(date):
    list_df=da.getDataFrame('product_list',str(date).replace('-',''))
    tags=da.rowGroupCount(list_df,'values')
    for tag in tags.keys()[:10]:
        print tag,tags.get(tag,0)

def init(datetime):
    global articles,products,order_product_counts,cart_product_counts,tags,\
            product_unique_visitor,article_unique_visitor,tag_unique_visitor
    product_df=da.getDataFrame('product',datetime)
    article_df=da.getDataFrame('article',datetime)
    tags_df=da.getDataFrame('product_list',datetime)
    products=da.rowGroupCount(product_df,'values')
    articles=da.rowGroupCount(article_df,'values')
    tags=da.rowGroupCount(tags_df,'values')
    order_product_counts=da.getOrderCounts(datetime)
    cart_product_counts=da.getCartCount(datetime)
    product_unique_visitor=da.getDfUniqueDevice(product_df,'values')
    article_unique_visitor=da.getDfUniqueDevice(article_df,'values')
    tag_unique_visitor=da.getDfUniqueDevice(tags_df,'values')

def getDataFileName(date,api_key,key=None):
    import Config
    if key:
        return '{0}/{1}_{2}{3}'.format(Config.getHomeDateDir(),date,api_key,key)
    else:
        import os
        fileNames=filter(lambda x:str(x).startswith(date+'_'+api_key),[filename for filename in os.listdir(Config.getHomeDateDir())])
        return map(lambda x:'{0}/{1}'.format(Config.getHomeDateDir(),x),fileNames)

def result(date,item_name,item_type,item_id,item_title):
    item_type=str(item_type).lower()
    if item_type == 'product':
        product_result(date,item_name,item_id,item_title)
    elif item_type == 'article':
        article_result(date,item_name,item_id,item_title)
    elif item_type == 'tag':
        tags_result(date,item_name,item_title)

def product_result(date,catogory_name,product_id,product_name):
    global products,cart_product_counts,order_product_counts,product_unique_visitor
    print '{7},{0},{1},{2},{3},{4},{5},{6}'.format( catogory_name,'product',\
            idu.decode_product(product_id),products.get(product_id,0),\
            cart_product_counts.get(product_id,0),order_product_counts.get(product_id,0),\
            product_unique_visitor.get(product_id,0),date)
    db.update_home_statics(date,catogory_name,'product',\
            idu.decode_product(product_id),products.get(product_id,0),\
            cart_product_counts.get(product_id,0),order_product_counts.get(product_id,0),\
            product_unique_visitor.get(product_id,0))

def article_result(date,catogory_name,article_id,article_name):
    global articles,article_unique_visitor
    print '{5},{0},{1},{2},{3},{4}'.format(catogory_name,'article',\
            idu.decode_article(article_id),articles.get(article_id,0),\
            article_unique_visitor.get(article_id,0),date)
    db.update_home_statics(date,catogory_name,'article',\
            idu.decode_article(article_id),articles.get(article_id,0),0,0,\
            article_unique_visitor.get(article_id,0))


def tags_result(date,catogory_name,tag_title):
    global tags,tag_unique_visitor
    print '{5},{0},{1},{2},{3},{4}'.format(catogory_name,'tag',tag_title,tags.get(tag_title,0),\
            tag_unique_visitor.get(tag_title,0),date)
    db.update_home_statics(date,catogory_name,'tag',tag_title,tags.get(tag_title,0),0,0,\
            tag_unique_visitor.get(tag_title,0))

def analyzeItem(item_name,item):
    return item.get('type','') ,item.get('id',''),item.get('name','') if item.get('name','') else item.get('title','')

def analyzeItemList(date,item_name,item_list):
    if not item_name == 'sections':
        for item in map(lambda x : analyzeItem(item_name,x),item_list):
            item_type,item_id,item_title=item
            result(date,item_name,item_type,item_id,item_title)
    else:
        for item in item_list:
            analyzeItemList(date,'sections'+'_'+item['name'],item['objects'])


def home_record(date,api_key='4def4d59'):
    fileNames = getDataFileName(date,api_key)
    if fileNames :
        for fileName in fileNames:
            with open(fileName,'r') as home_data_file:
                home_data=eval(home_data_file.read(),{'false': False, 'true': True, 'null': None})
                for key in home_data.keys():
                    if isinstance(home_data[key],list):
                        analyzeItemList(date,key,home_data[key])
    else:
        print 'no file match {0}_{1}'.format(date,api_key)


def data_record(date):
    strdate=str(date).replace('-','')
    init(strdate)
    product_record(date)
    home_record(strdate)

def main():
    import datetime,sys
    if '-i' in sys.argv:
        yestoday=datetime.date.today()-datetime.timedelta(days=1)
        data_record(yestoday)
    else:
        import log_analyze as la
        for date in la.getDates('2015,1,27','2015,1,27'):
            data_record(date)

if __name__ == '__main__':
    main()
