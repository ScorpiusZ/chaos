#! /usr/bin/env python
#coding:utf8
import data_analyze as da
import id_util as idu

def product_record(date):
    import configs.db as db
    product_df=da.getDataFrame('product',str(date).replace('-',''))
    products=da.rowGroupCount(product_df,'values')
    for product_id in products.keys():
        pv=products.get(product_id,0)
        product_id=idu.decode_product(product_id)
        if not db.update_product(product_id,pv,date):
            db.update_product(product_id,pv,date)
            print product_id,pv,date,'retry'
        else:
            print product_id,pv,date,'success'

def product_list_record(date):
    list_df=da.getDataFrame('product_list',str(date).replace('-',''))
    tags=da.rowGroupCount(list_df,'values')
    for tag in tags.keys()[:10]:
        print tag,tags.get(tag,0)


def main():
    import datetime,sys
    if '-i' in sys.argv:
        product_record(datetime.date.today()-datetime.timedelta(days=1))
    else:
        import log_analyze as la
        for date in la.getDates('2015,1,1','2015,1,2'):
            product_record(date)

if __name__ == '__main__':
    main()
