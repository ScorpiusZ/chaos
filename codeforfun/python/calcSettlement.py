#! /usr/bin/env python
#coding:utf8
import requests
import re
from datetime import date,timedelta

def getHtml(date):
    data_result=initApp([ '爱恋吧', '匿爱', '风月同城', '影缘遇上你', '缘来一线', '爱看美视频' ])
    url='http://e.qq.com/ec/api.php?mod=report&act=campaign&g_tk=1007011877&d_p=0.9904019145760685&callback=frameElement.callback&script&g_tk=1007011877'
    headers={
        'Content-Type':'application/x-www-form-urlencoded',
        'Cookie':'',
        }
    data='qzreferrer=http%3A%2F%2Fe.qq.com%2Fatlas%2F153094%2Freport%2Fcampaign%23&datetype=1&format=json&page=1&pagesize=20&fastdate=custom&sdate={date}&edate={date}&searchcname=&reportonly=0&_fastDate=false&callback=frameElement.callback%26script&owner=153094'.format(date=date)
    print date
    response=requests.post(url,headers=headers,data=data,timeout=5)
    content=response.content
    m=re.search('callback\((.*)\)',content)
    result=m.groups(0)[0]
    result=eval(result)
    advs=result['data']['list']
    for adv in advs:
        name=adv['campaignname']
        cost=adv['cost']
        print ' 名称  : {0}   花费 : {1} '.format(name,int(cost)/100.0 if cost!='-' else cost)
        for app_name in data_result.keys():
            if app_name in name and cost!='-':
                data_result[app_name]=data_result[app_name]+cost

    print '总计'
    for app_name in data_result.keys():
        print ' 名称 {0}  总花费 {1}'.format(app_name,int(data_result[app_name])/100.0)

def getDates(date_from,date_to):
    from_y,from_m,from_d=map(int,date_from.split(','))
    to_y,to_m,to_d=map(int,date_to.split(','))
    d_from=date(from_y,from_m,from_d)
    d_to=date(to_y,to_m,to_d)
    interval=d_to-d_from
    return [d_from+timedelta(days=x) for x in xrange(interval.days+1)]

def initApp(nameList):
    result={}
    for name in nameList:
        result[name]=0
    return result

def test():
    url='http://e.qq.com/ec/api.php?mod=report&act=adlist&g_tk=136358241&d_p=0.6894646440632641&callback=frameElement.callback&script&g_tk=136358241'
    headers={
        'Content-Type':'application/x-www-form-urlencoded',
        'Cookie':'',
        }
    data='qzreferrer=http%3A%2F%2Fe.qq.com%2Fatlas%2F275712%2Freport%2Forder&datetype=1&format=json&page=1&pagesize=20&sdate=2014-12-17&edate=2014-12-17&status=&fastdate=custom&searchtype=&searchname=&reportonly=0&product_type=&product_id=&callback=frameElement.callback%26script&owner=275712'
    response=requests.post(url,headers=headers,data=data,timeout=5)
    print response.content
    result=getResponseContent(response.content,'callback')
    #print result
    for adv in result['data']['list']:
        print adv['ordername'] ,adv['orderid']

def getResponseContent(content,match):
    pattern='{0}\((.*)\)'.format(match)
    if not content:
        return
    m=re.search('callback\((.*)\);',content)
    result=m.groups(0)[0]
    result=eval(result)
    return result

def getDetail(orderid):
    url='http://e.qq.com/ec/api.php?mod=report&act=getcrtsizedetail&g_tk=136358241&d_p=0.2254057547543198&orderid={0}&sdate=2014-12-17&edate=2014-12-17&page=1&pagesize=10&callback=_Callback&owner=275712'.format(orderid)
    headers={
        'Content-Type':'application/x-www-form-urlencoded',
        'Cookie':'',
        }
    print url
    response=requests.get(url,headers=headers)
    print response.content
    print
    print getResponseContent(response.content)
    #content=getResponseContent(response.content)
    #for item in content['data']['list']:
        #print item['time'],item['cost']


def main():
    #for date in getDates('2014,9,2','2014,9,4'):
        #getHtml(date)
    test()
    #getDetail(5904087)

if __name__ == '__main__':
    main()
