#! /usr/bin/env python
#coding:utf8
import data_analyze as da
import data_mining as dm
import pandas as pd
import id_util

LIMIT=20
#pr_format='{0:12},{1:12},{2:12},{3:12},{4:12}'
pr_format='{0},{1},{2},{3},{4}\n'
all_pr_format='{0},{1},{2},{3},{4},{5},{6}\n'

def product_statics(datetime,limit):
    data=''
    product_df=da.getDataFrame('product',datetime)
    condition=pd.notnull(product_df['device_id'])
    result=da.rowGroupCount(product_df[condition],'values')
    order_product_counts=da.getOrderCounts(datetime)
    cart_product_counts=da.getCartCount(datetime)
    product_ids=result.keys()
    data+=pr_format.format('date','product_id','product_pv','cart_count','order_count')
    for product_id in product_ids:
        data+=pr_format.format(datetime,id_util.decode_product(product_id),result.get(product_id,0),\
                cart_product_counts.get(product_id,0),\
                order_product_counts.get(product_id,0))
    data+=all_pr_format.format('sum',len(result.keys()),sum(result),\
            sum(cart_product_counts),\
            sum(order_product_counts),\
            da.getActiveUser(datetime),\
            da.getAllUser(datetime))
    da.write2CsvFile(datetime,'product',data)

def main():
    datetime='20150105'
    import sys
    if len(sys.argv)>1:
        datetime=sys.argv[1]
        product_statics(datetime,LIMIT)
    else:
        import log_analyze as la
        for date in la.getDates('2015,01,05','2015,01,07'):
            datetime=str(date).replace('-','')
            product_statics(datetime,LIMIT)

if __name__ == '__main__':
    main()
