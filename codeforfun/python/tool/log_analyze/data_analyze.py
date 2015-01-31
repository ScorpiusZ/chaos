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
    df=pd.read_csv(csvfile,names=volumn_names)
    return df[pd.notnull(df['device_id']) & pd.notnull(df['app_id'])]

def rowGroupCount(dataFrame,rowName):
    return dataFrame[rowName].value_counts()

def getProductCounts(products_list,product_id):
    return products_list.get(product_id,0)

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

def getUniqueDevice(datetime,api_type,group_key):
    item_df=getDataFrame(api_type,datetime)
    return item_df.groupby(group_key)['device_id'].unique().map(len)

def groupByCount(df,group_name,count_volumn_name):
    return df.groupby(group_name)[count_volumn_name].sum()

def getApiCountByApp(datetime,api_type):
    df=getDataFrame(api_type,datetime)
    df['count']=1
    return groupByCount(df,'app_id','count')

def getOneDayUnionDf(date,type_list):
    return map(lambda x:getDataFrame(x,date),type_list)

def getUnionDf(date_from,date_to,type_list):
    date_from,date_to=map(lambda x:datetime.datetime.strptime(x,'%Y%m%d'),[date_from,date_to])
    interval=date_to-date_from
    dates=[date_from+datetime.timedelta(days=x) for x in xrange(interval.days+1)]
    dates=map(lambda x:str(x).split(' ')[0].replace('-',''),dates)
    return map(lambda x:pd.concat(getOneDayUnionDf(x,type_list)),dates)

def getNewUserDevices(datetime):
    return getDataFrame('device',datetime)['device_id'].unique()

def getActiveUserdevices(datetime):
    return getUnionDf(datetime,datetime,dm.all_api_list)['device_id'].unique()

def getActiveUser(datetime):
    device_df=getDataFrame('device',datetime)
    condition=pd.notnull(device_df['device_id'])
    return len(device_df[condition]['device_id'].unique())

def getAllUser(datetime):
    home_df=getDataFrame('home',datetime)
    condition=pd.notnull(home_df['device_id'])
    return len(home_df[condition]['device_id'].unique())

def write2CsvFile(datetime,staticType,data):
    if data:
        import Config
        file_name='{0}/{1}_{2}.csv'.format(Config.getStaticDir(),datetime,staticType)
        with open(file_name,'w') as File:
            File.write(data)


def day_or_night(date):
    time=datetime.datetime.strptime(date.strip(),'%Y-%m-%d %H:%M:%S.%f')
    return 'day' if 9<=time.hour<=19 else 'night'

def getTagStatic(datetime,limit):
    print datetime
    tag_df=getDataFrame('product_list',datetime)
    print tag_df['values'].value_counts().sum()
    print tag_df['values'].value_counts()[:limit]

def test():
    datetime='20150105'
    #getUnionDf(datetime,'20150106',dm.all_api_list)
    #print getOneDayUnionDf(datetime,dm.all_api_list)
    #product_id='69ec4fcb3450ebd81be117f1bd2df0f4'
    #print order_df['new_time'].value_counts()
    #print getDataFrame('home',datetime)['values'].dropna().value_counts()
    #print order_df.sort('time',ascending=False).head(3)
    #print rowGroupCount(getDataFrame('product',datetime),'values')
    #print getProductViewCount(product_id,datetime)

def main():
    test()

if __name__ == '__main__':
    main()
