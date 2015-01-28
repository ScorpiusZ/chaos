#! /usr/bin/env python
#coding:utf8
import data_analyze as da
import pandas as pd
import api_util
import id_util

def getDataFileName(date,api_key,key=None):
    import Config
    if key:
        return '{0}/{1}_{2}{3}'.format(Config.getHomeDateDir(),date,api_key,key)
    else:
        import os
        fileNames=filter(lambda x:str(x).startswith(date+'_'+api_key),[filename for filename in os.listdir(Config.getHomeDateDir())])
        return map(lambda x:'{0}/{1}'.format(Config.getHomeDateDir(),x),fileNames)

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
    return item.get('type','') ,item.get('id',''),item.get('name','') if item.get('name','') else item.get('title','')

def product_result(product_id,product_name):
    global products,cart_product_counts,order_product_counts
    return 'product_id:{3},{0},{1},{2}\n'.format( products.get(product_id,0),\
            cart_product_counts.get(product_id,0),\
            order_product_counts.get(product_id,0),\
            id_util.decode_product(product_id))

def article_result(article_id,article_name):
    global articles
    product_ids=map(id_util.encode_product,api_util.getProductIdInArticle(article_id))
    result=map(lambda x :product_result(x,''),product_ids)
    return 'article_id:{2},{0}\n   {1}\n'.format(articles.get(article_id,0),\
            '\n '.join(result),\
            id_util.decode_article(article_id))

def tags_result(tag_title):
    global tags
    return 'tag_name:{1},{0}\n'.format(tags.get(tag_title,0),tag_title)

def result(item_type,item_id,item_title):
    item_type=str(item_type).lower()
    if item_type == 'product':
        return product_result(item_id,item_title)
    elif item_type == 'article':
        return article_result(item_id,item_title)
    elif item_type == 'tag':
        return tags_result(item_title)

def analyzeItemList(date,item_name,item_list):
    data=''
    if not item_name == 'sections':
        data+=item_name
        data+='\n'
        for item in map(lambda x : analyzeItem(item_name,x),item_list):
            item_type,item_id,item_title=item
            data+=result(item_type,item_id,item_title)
            data+='\n'
    else:
        for item in item_list:
            data+=analyzeItemList(date,'sections'+'_'+item['name'],item['objects'])
    return data


def analyzeHomeData(date,api_key='4def4d59'):
    init(date)
    fileNames = getDataFileName(date,api_key)
    if fileNames :
        for fileName in fileNames:
            data=''
            with open(fileName,'r') as home_data_file:
                home_data=eval(home_data_file.read(),{'false': False, 'true': True, 'null': None})
                for key in home_data.keys():
                    if isinstance(home_data[key],list):
                        data+=analyzeItemList(date,key,home_data[key])
                write_data_csv(fileName,data)
    else:
        print 'no file match {0}_{1}'.format(date,api_key)

def write_data_csv(fileName,data):
    import Config
    data_file_name='{0}/{1}_{2}.csv'.format(Config.getStaticDir(),str(fileName).split('/')[-1],'home')
    if data:
        with open(data_file_name,'w') as File:
            File.write(data)

def init(datetime):
    global articles,products,order_product_counts,cart_product_counts,tags
    product_df=da.getDataFrame('product',datetime)
    article_df=da.getDataFrame('article',datetime)
    tags_df=da.getDataFrame('product_list',datetime)
    products=da.rowGroupCount(product_df[pd.notnull(product_df['device_id'])],'values')
    articles=da.rowGroupCount(article_df[pd.notnull(article_df['device_id'])],'values')
    tags=da.rowGroupCount(tags_df[pd.notnull(tags_df['device_id'])],'values')
    order_product_counts=da.getOrderCounts(datetime)
    cart_product_counts=da.getCartCount(datetime)

def main():
    import datetime,sys
    date='20150105'
    if '-get' in sys.argv:
        date=datetime.datetime.now().strftime('%Y%m%d')
        getHomeData(date,'4def4d59')
    elif len(sys.argv)>1:
        date=sys.argv[1]
    analyzeHomeData(date)
    #getDataKey(date)

if __name__ == '__main__':
    main()
