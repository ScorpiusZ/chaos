#! /usr/bin/env python
#coding:utf8
import requests
from bs4 import BeautifulSoup
import urllib
import sys

def getHtmlContent(url):
    return requests.get(url,timeout=10).content

def qwys_get():
    for page in xrange(1,62):
        qwys_get_list(page)

def qwys_get_list(page):
    url='http://www.qiwenmi.com/qwys/{0}.html'
    url_root='http://www.qiwenmi.com{0}'
    html=getHtmlContent(url.format(page))
    soup=BeautifulSoup(html)
    page_lb=soup.findAll('div',class_='page_lb')
    divs=soup.findAll('div',class_='sublist')
    for div in divs:
        detail_url=url_root.format(div.h3.find('a').get('href'))
        qwys_detail_get(detail_url,url_root)


def qwys_detail_get(url,url_root):
    html=getHtmlContent(url)
    soup=BeautifulSoup(html)
    content_div=soup.find('div',class_='content')
    title=content_div.find('div',class_='content_tit')
    print title.text
    images=content_div.find('div',class_='content_pic small')
    #print images
    for link in images.findAll('a'):
        image_url=url_root.format(link.find('img').get('src'))
        print image_url
    content_p=''
    for p in images.findAll('p'):
        content_p+=p.text
    print content_p

def bmxz_get():
    for page in xrange(1,2):
        bmxz_get_list(page)

def bmxz_get_list(page):
    url='http://www.puahome.com/bbs/f-101-{0}.html'.format(page)
    url_root='http://www.puahome.com/bbs{0}'
    headers={
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36',
        'Cookie':' kvmi_2132_saltkey=J0AijZjR; kvmi_2132_lastvisit=1413789704; kvmi_2132_visitedfid=101; YJS=fe8e1ff0f4ea673fc5918d39b77b5142,MTQxMzc5NjkwNQ==; _gat=1; kvmi_2132_st_t=0%7C1413793522%7Caf83356ab50c15181ced25a705a58cc3; kvmi_2132_forum_lastvisit=D_101_1413793522; kvmi_2132_sid=gklFjZ; Hm_lvt_9f611a57eb6ed694c8e96cb075ecc0f6=1413793306; Hm_lpvt_9f611a57eb6ed694c8e96cb075ecc0f6=1413793524; _ga=GA1.2.1011294069.1413793306; kvmi_2132_lastact=1413793523%09connect.php%09check'
            }
    html=requests.get(url,headers=headers,timeout=10).content
    soup=BeautifulSoup(html)
    tag_ul=soup.find('ul',class_='plist')
    for li in tag_ul.findAll('li'):
        detail_url=url_root.format(li.find('a').get('href'))
        bmxz_get_detail(detail_url,url_root)
        break

def bmxz_get_detail(url,url_root):
    headers={
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36',
        'Referer':'http://www.puahome.com/bbs/f-101-1.html',
        'Cookie':'kvmi_2132_saltkey=J0AijZjR; kvmi_2132_lastvisit=1413789704; kvmi_2132_visitedfid=101; YJS=fe8e1ff0f4ea673fc5918d39b77b5142,MTQxMzc5NjkwNQ==; kvmi_2132_st_t=0%7C1413794002%7Cd08c33bada70d9d6509d646b8b9b8b11; kvmi_2132_forum_lastvisit=D_101_1413794002; kvmi_2132_st_p=0%7C1413795150%7C2e9b32ccd1ad9ddb2027523d485fffa7; kvmi_2132_viewid=tid_66892; kvmi_2132_sid=v6pcp6; Hm_lvt_9f611a57eb6ed694c8e96cb075ecc0f6=1413793306; Hm_lpvt_9f611a57eb6ed694c8e96cb075ecc0f6=1413795152; _ga=GA1.2.1011294069.1413793306; kvmi_2132_lastact=1413795151%09connect.php%09check'
            }
    html=requests.get(url,headers=headers,timeout=10).content
    soup=BeautifulSoup(html)
    print html
    content_tab=soup.find('table',class_='plhin')
    print content_tab

def gms_get(count):
    url='http://www.520guimi.com/mobi/v6/stream/threads_list.json'
    data='track={0}&fid=107&channel=1002005&client_version_code=10901&deviceId=A000004800AE17&auth=&pauth='
    track=''
    headers={
        'content-type':'application/x-www-form-urlencoded',
            }
    i=0
    while i<count:
        response=requests.post(url,headers=headers,data=data.format(track),timeout=10)
        content=eval(response.text)
        track=content['track']
        dataList=content['data']
        for item in dataList:
            i=i+1
            keys=item.keys()
            print
            print i
            if 'author' in keys:
                print item['author']['nickname']
            print item['extra']['topic']
            print item['content']
            if 'imgGroups' in keys:
                print item['imgGroups']
            print



def main():
    #qwys_get()
    #bmxz_get()
    gms_get(30)

if __name__ == '__main__':
    main()
