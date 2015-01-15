#! /usr/bin/env python
#coding:utf8
import pandas as pd
import data_mining as dm
import log_analyze as la

def getCsvFile(datetime):
    return '{0}/{1}.csv'.format(dm.CSV_DIR,datetime)

def getRootDataFrame(datetime):
    return pd.read_csv(getCsvFile(datetime),names=['time','api_tag','app_id','device_id','values'])

def getDataFrame(volumn_name,datetime):
    return getRootDataFrame(datetime)[getRootDataFrame(datetime)['api_tag']==volumn_name]

def getItemCount(item_id,datetime,item_tag):
    result=rowGroupCount(getDataFrame(item_tag,datetime),'values')
    return result[item_id] if item_id in result.keys() else 0

def getProductViewCount(product_id,datetime):
    return getItemCount(product_id,datetime,'product')

def getArticleViewCount(article_id,datetime):
    return getItemCount(product_id,datetime,'product')

def rowGroupCount(dataFrame,rowName):
    return dataFrame[rowName].value_counts()

def getUniqDevices(item_tag,datetime):
    return len(rowGroupCount(getDataFrame(item_tag,datetime),'device_id'))

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

def test():
    datetime='20150111'
    product_id='69ec4fcb3450ebd81be117f1bd2df0f4'
    print getUniqDevicesViewProduct(datetime)
    print getUniqDevicesCreateCart(datetime)
    #print showBriefStatics(datetime)
    #for date in la.getDates('2015,01,01','2015,01,14'):
        #print showBriefStatics(str(date).replace('-',''))
    #print getRootDataFrame(datetime)['api_tag'].value_counts()
    #print rowGroupCount(getDataFrame('product',datetime),'values')
    #print getProductViewCount(product_id,datetime)

def main():
    test()

if __name__ == '__main__':
    main()
