#! /usr/bin/env python
#coding:utf8
import requests
import re

API_ROOT='http://api.aihuo360.com/v2'

def list_unique(item_list):
    seen = set()
    seen_add = seen.add
    return [ x for x in item_list if not (x in seen or seen_add(x))]

def doGetRequest(url):
    try:
        response=requests.get(url)
        return response
    except:
        return ''

def get_article_detail(article_id):
    url='{0}{1}{2}'.format(API_ROOT,'/articles/',article_id)
    response=doGetRequest(url)
    return response

def getProductIdInHtml(html):
    pattern=re.compile(r'window.adultshop.openProduct\(([0-9]*)\)')
    macher=pattern.findall(html)
    return list_unique(macher) if macher else ''


def getProductIdInArticle(article_id):
    response=get_article_detail(article_id)
    if response:
        html=response.json()['body']
        return getProductIdInHtml(html) if html else ''
    else:
        return ''


def main():
    print getProductIdInArticle('6c4a632c33598c34f8bc6104f06a75d8')


if __name__ == '__main__':
    main()
