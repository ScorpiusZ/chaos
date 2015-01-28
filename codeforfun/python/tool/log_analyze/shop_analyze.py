#! /usr/bin/env python
#coding:utf8
import data_analyze as da
from collections import OrderedDict
import configs.db as db

#pr_format='{0:12},{1:12},{2:12},{3:12},{4:12},{5:12},{6:12},{7:12}'
pr_format='{0},{1},{2},{3},{4},{5},{6:},{7}'

LIMIT=20

def getShopStatics(datetime):
    print datetime
    data=''
    result=da.getUniqueDevice(datetime,'home','app_id')
    result_dict=dict((key,result[key])for key in result.keys())
    sorted_dict=OrderedDict(sorted(result_dict.items(),key=lambda item:item[1],reverse=True))
    app_names=db.getAppNames(sorted_dict.keys()[:LIMIT])
    device_df=da.getDataFrame('device',datetime)
    new_devices=da.getUniqueDevice(datetime,'device','app_id')
    articles=da.getApiCountByApp(datetime,'article')
    products=da.getApiCountByApp(datetime,'product')
    products_lists=da.getApiCountByApp(datetime,'product_list')
    orders=da.getApiCountByApp(datetime,'order')
    carts=da.getApiCountByApp(datetime,'cart')
    data+=pr_format.format('app_id','active_user','new_user','article','product','product_list','cart','order')
    for key,value in sorted_dict.items()[:LIMIT]:
        data+=pr_format.format(app_names.get(key,''),value,new_devices.get(key,0),\
                articles.get(key,0),products.get(key,0),\
                products_lists.get(key,0), carts.get(key,0),\
                orders.get(key,0))
    data+='sum\n'
    data+=pr_format.format(len(sorted_dict),sum(sorted_dict.values()),sum(new_devices),\
            sum(articles),sum(products),sum(products_lists),\
            sum(carts),sum(orders))
    da.write2CsvFile(datetime,'shop',data)

def main():
    import sys
    datetime='20150110'
    if len(sys.argv)>1:
        datetime=sys.argv[1]
        getShopStatics(datetime)
    else:
        getShopStatics(datetime)

if __name__ == '__main__':
    main()
