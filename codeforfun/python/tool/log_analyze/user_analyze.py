#! /usr/bin/env python
#coding:utf8
import data_analyze as da
import pandas as pd
import datetime

def getOrderedDeviceIds(datetime):
    order_df=da.getDataFrame('order',datetime)
    return order_df['device_id'].unique()

def getCartedDeviceIds(datetime):
    cart_df=da.getDataFrame('cart',datetime)
    return cart_df['device_id'].unique()

def targetDevicesDf(df,device_ids):
    return df[df['device_id'].isin(device_ids)]

def getTargetDevicesDfs(datetime,device_ids):
    import data_mining as dm
    all_dfs=map(lambda x:da.getDataFrame(x,datetime),dm.all_api_list)
    targetDevices_dfs=map(lambda x:targetDevicesDf(x,device_ids),all_dfs)
    return pd.concat(targetDevices_dfs)

def deviceActions(date,device_ids):
    all_df =getTargetDevicesDfs(date,device_ids)
    result=all_df['api_tag'].value_counts()
    actions=' '.join(map(lambda x:'{0}:{1}'.format(x,result.get(x,'')),result.keys()))
    devices=all_df['device_id'].unique()
    return devices,actions

def device_analyze(date,device_ids,days):
    today=datetime.datetime.strptime(date,'%Y%m%d')
    for date in [today+datetime.timedelta(days=x) for x in xrange(days+1)]:
        datestr=str(date).split(' ')[0].replace('-','')
        devices,actions=deviceActions(datestr,device_ids)
        print datestr,len(devices),actions

def report(date):
    print date
    print 'ordered_user'
    device_analyze(date,getOrderedDeviceIds(date),1)
    print 'cart_user'
    device_analyze(date,getCartedDeviceIds(date),1)

def main():
    date='20150105'
    report(date)
    #datetime='20150105'
    #ar_df=getDataFrame('article',datetime)
    #pr_df=getDataFrame('product',datetime)
    #home_df=getDataFrame('home',datetime)
    #pl_df=getDataFrame('product_list',datetime)
    #or_df=getDataFrame('order',datetime)
    #ca_df=getDataFrame('cart',datetime)
    #tv_df=getDataFrame('topic_view',datetime)
    #tc_df=getDataFrame('topic_create',datetime)
    #rp_df=getDataFrame('reply',datetime)
    #pm_df=getDataFrame('private_msg',datetime)
    #al_df=pd.concat([ar_df,pr_df,home_df,pl_df,or_df,ca_df,tv_df,tc_df,rp_df,pm_df])
    #al_df=al_df.sort('time',ascending=True)
    #print len(al_df)
    #print len(al_df['device_id'].unique())
    #grouped=al_df.groupby('device_id')
    #sum_all=len(grouped['api_tag'].agg(','.join).value_counts())
    #print sum_all
    #print grouped['api_tag'].agg(','.join).value_counts().map(lambda x: x/float(sum_all))[:50]

if __name__ == '__main__':
    main()
