#! /usr/bin/env python
#coding:utf8
import requests
import re


def getHtml(date):
    url='http://e.qq.com/ec/api.php?mod=report&act=campaign&g_tk=782042133&d_p=0.4388993347529322&callback=frameElement.callback&script&g_tk=782042133'
    headers={
        'Content-Type':'application/x-www-form-urlencoded',
        'Cookie':'gdt_cm_tag=6f8e3b798fcebb7-10b45e12-48dc-80b9-2c4cd02c942f74785d2fe6; RK=jDEzXtFEPE; pgv_info=ssid=s8009403742; pgv_pvid=1899652405; o_cookie=520095417; pgv_pvi=9923775488; pgv_si=s5717600256; qm_username=520095417; qm_sid=6642b654e822ca306e458b6f7031388b,cl_ydKsiwvwA.; ptui_loginuin=2773324502; pt2gguin=o2773324502; uin=o2773324502; skey=@efOB42lZH; ptisp=cnc; ptcz=4901417f295cd376e954274c4831167737b35ba910cc9d92b18bb42352c5ade3; firsttime=0',
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
        print ' 名称  : {0}   花费 : {1} '.format(adv['campaignname'],adv['cost'])

dates={
    '2014-09-01',
    '2014-09-02',
    '2014-09-03',
    '2014-09-04',
    '2014-09-05',
    '2014-09-06',
    '2014-09-07',
    '2014-09-08',
    '2014-09-09',
    '2014-09-10',
    '2014-09-11',
    '2014-09-12',
        }

def main():
    for date in dates:
        getHtml(date)

if __name__ == '__main__':
    main()
