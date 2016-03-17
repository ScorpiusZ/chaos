#! /usr/bin/env python
#coding:utf8
import requests
from random import random
from time import time
import subprocess

def get_wifi_pwds(ssids,bssids):
    # https://www.wifi4.cn/querys/#!H3C-2,H-AP-1,GeekPark-M/80F62E22E020,80F62E22DF90,A4560252C985
    url  = 'https://www.wifi4.cn/api/v2/?random={0}'.format(random())
    bssids =map(lambda x: x.replace(':','').upper(),bssids)
    data = 'ssids={0}&bssids={1}'.format(','.join(ssids),','.join(bssids))
    headers = {
        'content-type':'application/x-www-form-urlencoded; charset=UTF-8',
        'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116\
        Safari/537.36',
        'referer':'https://www.wifi4.cn/querys/',
        'x-requested-with':'XMLHttpRequest'
            }
    res = requests.post(url, data=data, headers=headers)
    result = res.json()
    if result.get('querys',''):
        return dict(zip(ssids,map(lambda e:result['querys'].get(e,{}).get('pwd',""),bssids)))
    else:
        print 'query error'
        print data
        print result
        return {}

def get_wifi_list():
    ignore_chars = '?#"\\'
    content = subprocess.check_output(['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport','-s'])
    result = {}
    for line in content.split('\n')[1:-1]:
        ssid,bssid = line.split()[0:2]
        if ':' in bssid and not(any(char in ssid for char in ignore_chars  )) :
            result[ssid] = bssid
    return result

def scan_wifi():
    print_format = '{0:32} {1:32} {2:32}'
    wifi_lists = get_wifi_list()
    ssids = wifi_lists.keys()
    bssids = wifi_lists.values()
    result = get_wifi_pwds(ssids,bssids)
    print print_format.format('ssid','bssid','password')
    for ssid,bssid in wifi_lists.items():
        print print_format.format(ssid,bssid,result[ssid] if result.get(ssid,'') else '?????')


def main():
    # params = get_wifi_list()
    # ssids = ['imo','GeekPark-M','GeekPark','H3C-3-hofo','hofo-l','H3C-2']
    # bssids = ['6c:70:9f:e6:90:40','a4:56:02:52:c9:85','c4:04:15:29:7c:38','fc:d7:33:d2:66:12','b0:c7:45:2e:b6:e4','80:f6:2e:22:e0:30']
    # for k,v in get_wifi_pwds(ssids,bssids).items():
        # print k,v
    scan_wifi()

if __name__ == '__main__':
    main()

