#! /usr/bin/env python
#coding:utf8
import pandas as pd
import data_mining as dm
import log_analyze as la
import id_util as idu
import datetime

def getCsvFile(datetime):
    return '{0}/{1}.csv'.format(dm.CSV_DIR,datetime)

def getRootDataFrame(datetime):
    return pd.read_csv(getCsvFile(datetime),names=['time','api_tag','app_id','device_id','values'])

def getDataFrame(volumn_name,datetime):
    return getRootDataFrame(datetime)[getRootDataFrame(datetime)['api_tag']==volumn_name]

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

def showBriefStatics(datetime):
    return getRootDataFrame(datetime)['api_tag'].value_counts()

def getProductCounts(products_list,product_id):
    return products_list.get(product_id,0)

def showProductPV(datetime,limit):
    print datetime
    order_product_counts=getOrderCounts(datetime)
    cart_product_counts=getCartCount(datetime)
    result=rowGroupCount(getDataFrame('product',datetime),'values')
    for product_id in result[:limit].keys():
        print '{0:10},{1:10},{3:10},{2}'\
                .format(idu.decode_product(product_id).strip(),result[product_id],\
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
    return getOrderOrCartCount(datetime,'orders')

def getCartCount(datetime):
    return getOrderOrCartCount(datetime,'cart')

def day_or_night(date):
    time=datetime.datetime.strptime(date.strip(),'%Y-%m-%d %H:%M:%S.%f')
    return 'day' if 9<=time.hour<=19 else 'night'


def test():
    datetime='20150111'
    product_id='69ec4fcb3450ebd81be117f1bd2df0f4'
    order_df=getDataFrame('orders',datetime)
    order_df['new_time']=order_df.time.apply(day_or_night)
    print order_df['new_time'].value_counts()
    #print order_df.sort('time',ascending=False).head(3)
    #showProductPV(datetime,50)
    #print getUniqDevicesVi,20ewProduct(datetime)
    #print getUniqDevicesCreateCart(datetime)
    #print showBriefStatics(datetime)
    #showProductPV('20150115',50)
    #for date in la.getDates('2015,01,14','2015,01,15'):
        #showProductPV(str(date).replace('-',''),50)
    #print getRootDataFrame(datetime)['api_tag'].value_counts()
    #print rowGroupCount(getDataFrame('product',datetime),'values')
    #print getProductViewCount(product_id,datetime)

def main():
    test()

if __name__ == '__main__':
    main()
