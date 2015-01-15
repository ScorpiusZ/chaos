#! /usr/bin/env python
#coding:utf8
import pandas as pd
import data_mining as dm

def getCsvFile(datetime):
    return '{0}/{1}.csv'.format(dm.CSV_DIR,datetime)

def getRootDataFrame(datetime):
    return pd.read_csv(getCsvFile(datetime),names=['time','api_tag','app_id','device_id','values'])

def getDataFrame(volumn_name,datetime):
    return getRootDataFrame(datetime)[getRootDataFrame(datetime)['api_tag']==volumn_name]

def getProductViewCount(product_id,datetime):
    product_df=getDateFrame('product',datetime)

def test():
    datetime='20150105'
    print getDataFrame('product',datetime)
    #csvFile=dm.CSV_DIR+'/20150105.csv'
    #df=pd.read_csv(csvFile,names=)
    ##print df['api_tag'].value_counts()
    #article_df=df[df['api_tag'] == 'article']
    #product_df=df[df['api_tag'] == 'product']
    #order_df=df[df['api_tag'] == 'orders']
    #cart_df=df[df['api_tag'] == 'cart']
    ##print article_df['values'].value_counts()
    ##print product_df['values'].value_counts()
    ##product=product_df[product_df['values'] == '0a33a205d9b71e043cac7390a3a2e4df']['values'].value_counts()
    ##print product['0a33a205d9b71e043cac7390a3a2e4df']
    ##print cart_df['device_id'].value_counts()
    #print order_df['values'].value_counts()

def main():
    test()

if __name__ == '__main__':
    main()
