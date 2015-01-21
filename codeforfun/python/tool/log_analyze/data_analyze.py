#! /usr/bin/env python
#coding:utf8
import pandas as pd
import id_util as idu
import datetime
import Config
import data_mining as dm

volumn_names=['time','api_tag','app_id','device_id','values']

def getDataFrame(api_type,datetime):
    import os
    csvfile=dm.getCsvFile(datetime,api_type)
    if not os.path.exists(csvfile):
        dm.getData(datetime,[api_type])
    return pd.read_csv(csvfile,names=volumn_names)

def getItemCount(item_id,datetime,item_tag):
    result=rowGroupCount(getDataFrame(item_tag,datetime),'values')
    return result.get(item_id,0)

def getProductViewCount(product_id,datetime):
    return getItemCount(product_id,datetime,'product')

def getArticleViewCount(article_id,datetime):
    return getItemCount(article_id,datetime,'article')

def rowGroupCount(dataFrame,rowName):
    return dataFrame[rowName].value_counts()

def getUniqDevices(item_tag,datetime):
    return len(getDataFrame(item_tag,datetime)['device_id'].unique())

def getUniqDevicesViewProduct(datetime):
    return getUniqDevices('product',datetime)

def getUniqDevicesViewArticle(datetime):
    return getUniqDevices('article',datetime)

def getUniqDevicesCreateOrders(datetime):
    return getUniqDevices('orders',datetime)

def getUniqDevicesCreateCart(datetime):
    return getUniqDevices('cart',datetime)

def getProductCounts(products_list,product_id):
    return products_list.get(product_id,0)

def showProductPV(datetime,limit):
    print datetime
    order_product_counts=getOrderCounts(datetime)
    cart_product_counts=getCartCount(datetime)
    result=rowGroupCount(getDataFrame('product',datetime),'values')
    for product_id in result[:limit].keys():
        print '{0:10},{1:10},{3:10},{2}'\
                .format(idu.decode_product(product_id),result[product_id],\
                getProductCounts(order_product_counts,product_id),\
                getProductCounts(cart_product_counts,product_id))

def getProductList(datetime,key_name):
    product_ids_list=[]
    for product_ids in getDataFrame(key_name,datetime)['values'].dropna():
        for product in product_ids.split(':'):
            product_ids_list.append(product)
    return product_ids_list

def getOrderOrCartCount(datetime,key_name):
    df=pd.Series(getProductList(datetime,key_name),name='values')
    return df.value_counts()

def getOrderCounts(datetime):
    return getOrderOrCartCount(datetime,'order')

def getCartCount(datetime):
    return getOrderOrCartCount(datetime,'cart')

def day_or_night(date):
    time=datetime.datetime.strptime(date.strip(),'%Y-%m-%d %H:%M:%S.%f')
    return 'day' if 9<=time.hour<=19 else 'night'


def test():
    datetime='20150105'
    #product_id='69ec4fcb3450ebd81be117f1bd2df0f4'
    #print order_df['new_time'].value_counts()
    #print getDataFrame('home',datetime)['values'].dropna().value_counts()
    #print order_df.sort('time',ascending=False).head(3)
    #showProductPV(datetime,50)
    print getUniqDevicesCreateCart(datetime)
    #showProductPV('20150115',50)
    #print rowGroupCount(getDataFrame('product',datetime),'values')
    #print getProductViewCount(product_id,datetime)

def main():
    test()

if __name__ == '__main__':
    main()
