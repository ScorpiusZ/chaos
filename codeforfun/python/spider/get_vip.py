#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wei'

import urllib2

from bs4 import BeautifulSoup


def account_data(article_url):
    html = urllib2.urlopen(article_url).read()
    soup = BeautifulSoup(html, 'html.parser')
    tag_span = soup.find_all("span", attrs={"style": "color: #339966;"})
    for content in tag_span:
            title = content.get_text().encode('UTF-8')
            print(title)

def getVIP(webSiteName,webSite,depth=1):
    html = urllib2.urlopen(webSite).read()
    soup = BeautifulSoup(html, 'html.parser')
    if not soup.find_all('article'):
        return ''
    print webSiteName,webSite
    article_urls = soup.find_all('article')[0].find_all('a')[0:depth]
    for a in article_urls:
        account_data(a.get('href'))


def get_video_sites():
    url = 'http://www.vipfenxiang.com'
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)
    links=soup.find_all('ul','nav')[0].find_all('a')
    return map(lambda tag: (tag.string,tag.get('href')),links)

def main():
    print get_video_sites()
    for site in get_video_sites():
        getVIP(site[0],site[1],3)
    #print("==========优酷==========")
    #getVIP("youku")
    #print("==========爱奇艺==========")
    #getVIP("iqiyi")
    #print("====================")
    #getVIP("iqiyi")

if __name__ == '__main__':
    main()

