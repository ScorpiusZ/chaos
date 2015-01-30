#! /usr/bin/env python
#coding:utf8
import data_analyze as da
import pandas as pd
import datetime
#import configs.db as db

def getOrderedDeviceIds(datetime):
    order_df=da.getDataFrame('order',datetime)
    return order_df['device_id'].unique()

def getCartedDeviceIds(datetime):
    cart_df=da.getDataFrame('cart',datetime)
    return cart_df['device_id'].unique()

def targetDevicesDf(df,device_ids):
    return df[df['device_id'].isin(device_ids)]

def getOnExpressDevicesIds(datetime):
    states=['客户拒签，原件返回','客户签收，订单完成','已发货，准备收货']
    return getDeviceIdsByState(datetime,states)

def getRejectDevicesIds(datetime):
    states=['客户拒签，原件返回','']
    return getDeviceIdsByState(datetime,states)

def getSignedDevicesIds(datetime):
    states=['客户签收，订单完成']
    return getDeviceIdsByState(datetime,states)

def getAbandonDevicesIds(datetime):
    states=['客户放弃，订单取消']
    return getDeviceIdsByState(datetime,states)

def getProgressedDevicesIds(datetime):
    states=['正在处理']
    return getDeviceIdsByState(datetime,states)

def getCantContactDevicesIds(datetime):
    states=['无法联系客户，订单取消']
    return getDeviceIdsByState(datetime,states)

def getNotOneSelfDevicesIds(datetime):
    states=['非本人下单，已取消','非本人下单，订单取消']
    return getDeviceIdsByState(datetime,states)

def getDeviceIdsByState(date,states):
    date=datetime.datetime.strptime(date,'%Y%m%d')
    return db.getOrderDeviceIds(date,states)

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
        print '{0},{1},{2}'.format(datestr,len(devices),actions)

def order_report(date):
    days=6
    print date
    print '生成购物车'
    device_analyze(date,getCartedDeviceIds(date),days)
    print '下单用户'
    device_analyze(date,getOrderedDeviceIds(date),days)
    print '已经发货用户'
    device_analyze(date,getOnExpressDevicesIds(date),days)
    print '客户拒签'
    device_analyze(date,getRejectDevicesIds(date),days)
    print '客户签收'
    device_analyze(date,getSignedDevicesIds(date),days)
    print '正在处理  订单'
    device_analyze(date,getProgressedDevicesIds(date),days)
    print ' 无法联系订单'
    device_analyze(date,getCantContactDevicesIds(date),days)
    print '非本人下单'
    device_analyze(date,getNotOneSelfDevicesIds(date),days)

def getCommunityDfs(date,device_ids):
    c_list=['topic_list','topic_view','topic_create','private_msg','reply','topic_like','topic_follow']
    all_dfs=map(lambda x:da.getDataFrame(x,date),c_list)
    targetDevices_dfs=map(lambda x:targetDevicesDf(x,device_ids),all_dfs)
    return pd.concat(targetDevices_dfs)

def community_action(date,device_ids):
    community_dfs=getCommunityDfs(date,device_ids)
    result=community_dfs['api_tag'].value_counts()
    actions=' '.join(map(lambda x:'{0}:{1}'.format(x,result.get(x,'')),result.keys()))
    devices=community_dfs['device_id'].unique()
    return devices,actions

def community_analyze(date,device_ids,days):
    today=datetime.datetime.strptime(date,'%Y%m%d')
    for date in [today+datetime.timedelta(days=x) for x in xrange(days+1)]:
        datestr=str(date).split(' ')[0].replace('-','')
        devices,actions=community_action(datestr,device_ids)
        print '{0},{1},{2}'.format(datestr,len(devices),actions)

def getNewUser(date):
    device_df=da.getDataFrame('device',date)
    return device_df['device_id'].unique()

def community_report(date):
    days=1
    new_devices=getNewUser(date)
    print '{1} New User:{0}'.format(len(new_devices),date)
    community_analyze(date,new_devices,days)

def main():
    date='20150106'
    import sys
    if len(sys.argv)>1:
        date=sys.argv[1]
    #order_report(date)
    community_report(date)
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
