#! /usr/bin/env python
#coding:utf8
import data_analyze as da
import id_util as idu

def product_record(date):
    import MySQLdb
    data_db=MySQLdb.connect(host='localhost',user='root',passwd='root',port=3306,db='my_db',charset='utf8')
    product_df=da.getDataFrame('product',str(date).replace('-',''))
    products=da.rowGroupCount(product_df,'values')
    cursor=data_db.cursor()
    for product_id in products.keys()[:10]:
        pv=products.get(product_id,0)
        sql='update um_products_info set _pv={0} where _pid={1} and DATE(_datetime)=\'{2}\''.format(pv,product_id,date)
        sql_home='update um_homepage set _pv = {0} where _d_id=4 and _description={1} and DATE(_datetime)=\'{2}\''.format(pv,product_id,date)
        cursor.execute(sql)
        cursor.execute(sql_home)
        db.commit()
    cursor.close()
    db.close()

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
