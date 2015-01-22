#! /usr/bin/env python
#coding:utf8
import data_analyze as da
import data_mining as dm
import api_util
import id_util

show_format='article_id:{0:10},view_count: {1:10}, product_id:{2:10}\
        view_count:{3:10}, cart_count:{4:6},order_count{5:6}, unique_device:{6}'
LIMIT=20

def article_statics(datetime,limit):
    print datetime
    product_view_counts=da.rowGroupCount(da.getDataFrame('product',datetime),'values')
    order_product_counts=da.getOrderCounts(datetime)
    cart_product_counts=da.getCartCount(datetime)
    result=da.rowGroupCount(da.getDataFrame('article',datetime),'values')
    for article_id in result[:limit].keys():
        product_ids=api_util.getProductIdInArticle(article_id)
        unique_device_num=article_unique_device_num(datetime,article_id)
        if product_ids:
            for product_id in product_ids:
                print show_format.format(id_util.decode_article(article_id),result[article_id],product_id,\
                        da.getProductCounts(product_view_counts,id_util.encode_product(product_id)),\
                        da.getProductCounts(cart_product_counts,id_util.encode_product(product_id)),\
                        da.getProductCounts(order_product_counts,id_util.encode_product(product_id)),\
                        unique_device_num)
        else:
            print show_format.format(id_util.decode_article(article_id),result[article_id],0,0,0,0,unique_device_num)


def init(datetime):
    import os
    init_list=[]
    for api_type in ['article','product','order','cart']:
        if not os.path.exists(dm.getCsvFile(datetime,api_type)):
            init_list.append(api_type)
    if init_list:
        dm.getData(datetime,init_list)

def article_unique_device_num(datetime,article_id):
    article_df=da.getDataFrame('article',datetime)
    return len(article_df[article_df['values'] == article_id]['device_id'].dropna().unique())

def main():
    datetime='20150114'
    import sys
    if len(sys.argv)>1:
        datetime=sys.argv[1]
        init(datetime)
        article_statics(datetime,LIMIT)
    else:
        import log_analyze as la
        for date in la.getDates('2015,01,11','2015,01,15'):
            datetime=str(date).replace('-','')
            init(datetime)
            article_statics(datetime,LIMIT)

if __name__ == '__main__':
    main()
