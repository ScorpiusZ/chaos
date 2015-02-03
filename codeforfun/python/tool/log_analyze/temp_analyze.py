#! /usr/bin/env python
#coding:utf8
import data_analyze as da
import configs.db as db
import datetime as dt

pr_format='{5},{0},{1},{2},{3},{4}'

def product_pv_statics(date):
    #print pr_format.format('new','active','pv','new_user_order','all_order','date')
    home_df,device_df,product_df,order_df=da.getOneDayUnionDf(date,['home','device','product','order'])
    new_user_devices=device_df['device_id'].unique()
    return pr_format.format(len(home_df['device_id'].unique()),\
            len(new_user_devices),\
            len(product_df),\
            len(order_df[order_df['device_id'].isin(new_user_devices)]),\
            len(order_df),date)

def every_report(date):
    product_df=da.getDataFrame('product',date)
    print_patter='{5},{0},{1},{2},{3},{4}'
    print print_patter.format('pv','order_all','order_rate','dealed_order','avg_order_price','date')
    datetime = dt.datetime.strptime(date,'%Y%m%d')
    order_all=db.get_all_order_sum(datetime)
    order_dealed=db.get_dealed_order_sum(datetime)
    print print_patter.format(len(product_df),order_all,\
            order_dealed/float(order_all),order_dealed,\
            db.avg_dealed_order_price(datetime,datetime),date)


def main():
    import log_analyze as la
    for date in la.getDates('2015,2,1','2015,2,2'):
        print every_report(str(date).replace('-',''))

if __name__ == '__main__':
    main()
