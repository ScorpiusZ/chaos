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
        'Cookie':' gdt_cm_tag=506de8314d5c8379-19208565-46ec-8d49-189601ab147cedbfc4b83d3; o_cookie=520095417; pgv_pvid=576081791; pgv_info=ssid=s4797060240; RK=Tf07quaQnd; pgv_pvi=5391354880; pgv_si=s1404079104; firsttime=0; zzpaneluin=; zzpanelkey=; verifysession=h028Zd0AxM4yqC592Y9H81VGgbRwRjfJ6G3DdwXm-QBvx1f3SBvQluzrz9_q4Ps3hlSWX9Tv8KW8bqPMc2MV2Kzlw**; ptui_loginuin=2773324502; pt2gguin=o2773324502; uin=o2773324502; skey=@S0MUKKw4z; ptisp=os; ptcz=acb5099a80ee7ff8edb4a9f71c3e056580dc74dc5144beb11712019b3387d316 ',
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

def main():
    for date in getDates('2014,9,2','2014,9,4'):
        getHtml(date)

if __name__ == '__main__':
    main()
