#! /usr/bin/env python
#coding:utf8
import data_analyze as da
import data_mining as dm
import api_util
import id_util
import configs.db as db

show_format='article_id:{0:10},view_count: {1:10}, product_id:{2:10}\
        view_count:{3:10}, cart_count:{4:6},order_count{5:6}, unique_device:{6}'
LIMIT=20

def article_statics(datetime,limit):
    print datetime
    product_view_counts=da.rowGroupCount(da.getDataFrame('product',datetime),'values')
    order_product_counts=da.getOrderCounts(datetime)
    cart_product_counts=da.getCartCount(datetime)
    result=da.rowGroupCount(da.getDataFrame('article',datetime),'values')
    article_ids=result[:limit].keys()
    article_unique_device_counts=da.getUniqueDevice(datetime,'article','values')
    for article_id in article_ids:
        product_ids=api_util.getProductIdInArticle(article_id)
        unique_device_num=article_unique_device_counts.get(article_id,0)
        if product_ids:
            for product_id in product_ids:
                print show_format.format(id_util.decode_article(article_id),result[article_id],product_id,\
                        da.getProductCounts(product_view_counts,id_util.encode_product(product_id)),\
                        da.getProductCounts(cart_product_counts,id_util.encode_product(product_id)),\
                        da.getProductCounts(order_product_counts,id_util.encode_product(product_id)),\
                        unique_device_num)
        else:
            print show_format.format(id_util.decode_article(article_id),result[article_id],0,0,0,0,unique_device_num)

def save_data(datetime,limit):
      product_view_counts=da.rowGroupCount(da.getDataFrame('product',datetime),'values')
      order_product_counts=da.getOrderCounts(datetime)
      cart_product_counts=da.getCartCount(datetime)
      result=da.rowGroupCount(da.getDataFrame('article',datetime),'values')
      article_ids=result.keys()[:limit]
      for article_id in article_ids:
          product_ids=api_util.getProductIdInArticle(article_id)
          if product_ids:
              for product_id in product_ids:
                  db.save_article_data(datetime,id_util.decode_article(article_id),result[article_id],product_id,\
                          da.getProductCounts(product_view_counts,id_util.encode_product(product_id)),\
                          da.getProductCounts(cart_product_counts,id_util.encode_product(product_id)),\
                          da.getProductCounts(order_product_counts,id_util.encode_product(product_id)))

          else:
              db.save_article_data(datetime,id_util.decode_article(article_id),result[article_id],0,0,0,0)

def init(datetime):
    csvfiles=map(lambda x:dm.getCsvFile(datetime,x),dm.all_api_list)
    import os
    if not all(map(os.path.exists,csvfiles)):
        dm.getData(datetime,dm.all_api_list)

def article_unique_device_num(datetime,article_id):
    return da.getUniqueDevice(datetime,'article','values').get(article_id,0)

def main():
    datetime='20150105'
    import sys
    if len(sys.argv)>1:
        datetime=sys.argv[1]
        init(datetime)
        article_statics(datetime,LIMIT)
    else:
        import datetime as dt
        yestoday_date=dt.date.today()-dt.timedelta(days=1)
        yestoday=yestoday_date.strftime('%Y%m%d')
        init(yestoday)
        save_data(yestoday,10)


if __name__ == '__main__':
    main()
