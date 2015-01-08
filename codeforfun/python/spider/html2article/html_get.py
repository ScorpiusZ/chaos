#! /usr/bin/env python
#encoding:utf8
import requests
from bs4 import BeautifulSoup
import ArticleDao

root_url='http://image.yepcolor.com/sm/{0}'

def getRelateUrlRoot(url):
    return '/'.join(url.split('/')[0:-1])+'/'

def dealHtml(tags,link_url):
    response=doGetRequest(link_url)
    if response:
        html=response.content
    else:
        return
    soup=BeautifulSoup(html)
    root=getRelateUrlRoot(link_url)
    for img in soup.findAll('img'):
        img['src']=root+img['src']
        #print img['src']
    ArticleDao.write_a_article(soup.title.string,tags,str(soup))


def parseHtml(tags,html):
    soup=BeautifulSoup(html)
    if soup.findAll('a'):
        for link in soup.findAll('a'):
            link_url=root_url.format(link.get('href'))
            print link_url
            if link_url.lower().endswith('.html'):
                getHomeHtml(tags+','+soup.title.string if tags else soup.title.string,link_url)
            elif link_url.lower().endswith('.htm'):
                dealHtml(tags+','+soup.title.string if tags else soup.title.string,link_url)
            else:
                #useless link_url
                pass

def doGetRequest(url):
    try:
        response=requests.get(url)
        return response
    except:
        print 'url {0} request timeout'.format(url)
        return

def getHomeHtml(tags,url):
    response=doGetRequest(url)
    if response:
        html=response.content
        parseHtml(tags,html)
    else:
        return

def main():
    url='http://image.yepcolor.com/sm/wsdetail.html'
    #url='http://image.yepcolor.com/sm/chanpinbaike/fangzhendaomo.htm'
    getHomeHtml('',url)
    #dealHtml('',url)

if __name__ == '__main__':
    main()
