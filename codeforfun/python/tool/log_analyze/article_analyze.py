#! /usr/bin/env python
#coding:utf8
import data_analyze as da
import api_util
import id_util

show_format='article_id:{0:10},view_count: {1:10}, product_id:{2:10}\
        view_count:{3:10}, cart_count:{4:6},order_count{5:6}'
LIMIT=20

def article_statics(datetime,limit):
    print datetime
    product_view_counts=da.rowGroupCount(da.getDataFrame('product',datetime),'values')
    order_product_counts=da.getOrderCounts(datetime)
    cart_product_counts=da.getCartCount(datetime)
    result=da.rowGroupCount(da.getDataFrame('article',datetime),'values')
    for article_id in result[:limit].keys():
        product_ids=api_util.getProductIdInArticle(article_id)
        if product_ids:
            for product_id in product_ids:
                print show_format.format(id_util.decode_article(article_id),result[article_id],product_id,\
                        da.getProductCounts(product_view_counts,id_util.encode_product(product_id)),\
                        da.getProductCounts(cart_product_counts,id_util.encode_product(product_id)),\
                        da.getProductCounts(order_product_counts,id_util.encode_product(product_id)))
        else:
            print show_format.format(id_util.decode_article(article_id),result[article_id],0,0,0,0)


def main():
    datetime='20150114'
    import sys
    if len(sys.argv)>1:
        datetime=sys.argv[1]
        article_statics(datetime,LIMIT)
    else:
        import log_analyze as la
        for date in la.getDates('2015,01,11','2015,01,15'):
            article_statics(str(date).replace('-',''),LIMIT)

if __name__ == '__main__':
    main()
