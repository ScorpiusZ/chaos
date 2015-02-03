#! /usr/bin/env python
#coding:utf8
import data_analyze as da

def product_record(date):
    import id_util,configs.db as idu,db
    product_df=da.getDataFrame('product',str(date).replace('-',''))
    products=da.rowGroupCount(product_df,'values')
    for product_id in products.keys()[:10]:
         db.update_product(idu.decode_product(product_id),products.get(product_id,0),date)

def product_list_record(date):
    list_df=da.getDataFrame('product_list',str(date).replace('-',''))
    tags=da.rowGroupCount(list_df,'values')
    for tag in tags.keys()[:10]:
        print tag,tags.get(tag,0)


def main():
    import log_analyze as la
    for date in la.getDates('2015,1,1','2015,1,2'):
        product_record(date)

if __name__ == '__main__':
    main()
