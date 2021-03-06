#! /usr/bin/env python
#coding:utf8
import data_analyze as da
import pandas as pd
import datetime
import configs.db as db

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
    all_dfs=da.getOneDayUnionDf(datetime,dm.all_api_list)
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
    all_device=[]
    for date in [today+datetime.timedelta(days=x) for x in xrange(days+1)]:
        datestr=str(date).split(' ')[0].replace('-','')
        devices,actions=deviceActions(datestr,device_ids)
        if date.day != today.day:
            all_device=all_device+devices.tolist()
        print '{0},{1},{2}'.format(datestr,len(devices),actions)
    print 'user remains,'+str(len(list(set(all_device))))

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
    all_dfs=da.getOneDayUnionDf(date,c_list)
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

def getActiveUserdevices(date):
    c_list=['topic_list','topic_view','topic_create','private_msg','reply','topic_like','topic_follow']
    return pd.concat(da.getOneDayUnionDf(date,c_list))['device_id'].unique()

def community_report(date):
    days=6
    new_devices=getNewUser(date)
    print '{1} New User:{0}'.format(len(new_devices),date)
    community_analyze(date,new_devices,days)
    active_devices=getActiveUserdevices(date)
    print '{1} Active User:{0}'.format(len(active_devices),date)
    community_analyze(date,active_devices,days)


def combine(x):
    x_list=str(x).split(',')
    return ','.join(list(set(x_list)))

def getViewProductType(uuid,actions):
    if not uuid or not actions :
        return
    action_list=actions.split(' , ')
    api_key,device_id=uuid.split(' ')
    from_type=''
    result=[]
    for action in action_list:
        try:
            time,api_type,value=action.split('&')
            if api_type == 'home' :
                from_type='home'
            elif api_type == 'product_list':
                from_type=value
            elif api_type == 'product':
               result.append((api_key,device_id,time,api_type,value,from_type))
        except:
            continue
    return result

def product_report(date):
    api_list=['product_list','home','product']
    #api_list=['home','product','article','product_list','cart','order','topic_list','topic_view','topic_create','private_msg','reply','topic_like','topic_follow','device']
    al_df=pd.concat(da.getOneDayUnionDf(date,api_list))
    al_df=al_df.sort('time',ascending=True)
    al_df['action']=al_df['time']+'&'+al_df['api_tag']+'&'+al_df['values'].map(str)
    al_df['uuid']=al_df['app_id']+' '+al_df['device_id']
    grouped=al_df.groupby('uuid')
    actions=grouped['action'].agg(' , '.join)
    result=grouped['api_tag'].agg(','.join).map(combine).value_counts()
    total=sum(result)
    typed_product_list=[]
    for key in actions.keys():
        typed_product_list+=getViewProductType(key,actions.get(key,''))
    result_df=pd.DataFrame(typed_product_list,columns=['api_key','device_id','time','api_type','value','from_type'])
    result_df['count']=1
    typed_product_list=result_df.groupby(['value','from_type'])['count'].sum()
    print type(typed_product_list)
    total=0
    for key in typed_product_list.keys():
        product_id,from_type=key
        num=typed_product_list.get(key,0)
        total+=num
        print product_id,from_type,num
    #for api_key,device_id,time,api_type,value,from_type in typed_product_list:
        #print api_key,device_id,time,api_type,value,from_type


def main():
    date='20150204'
    import sys
    if len(sys.argv)>1:
        date=sys.argv[1]
    #order_report(date)
    #print len(da.getDataFrame('product',date))
    product_report(date)
    #community_report(date)
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
