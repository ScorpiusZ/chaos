#! /usr/bin/env python
#coding:utf8
import data_analyze as da

pr_format='{5},{0},{1},{2},{3},{4}'

def product_pv_statics(date):
    #print pr_format.format('new','active','pv','new_user_order','all_order','date')
    home_df,device_df,product_df,order_df=da.getOneDayUnionDf(date,['home','device','product','order'])
    new_user_devices=device_df['device_id'].unique()
    return pr_format.format(len(home_df['device_id'].unique()),\
            len(new_user_devices),\
            len(product_df),\
            len(order_df[order_df['device_id'].isin(new_user_devices)]),\
            len(order_df),\
            date)

def main():
    import log_analyze as la
    for date in la.getDates('2015,1,26','2015,1,29'):
        print product_pv_statics(str(date).replace('-',''))

if __name__ == '__main__':
    main()
