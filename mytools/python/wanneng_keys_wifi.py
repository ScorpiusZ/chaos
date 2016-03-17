#! /usr/bin/env python
#coding:utf8
import requests
import hashlib
from collections import OrderedDict
from Crypto.Cipher import AES
import subprocess
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

pwd_params = { 'och': 'wandoujia',
           'ii': '',
           'appid': '0001',
           'pid': 'qryapwd:commonswitch',
           'lang': 'cn',
           'v': '58',
           'uhid': 'a0000000000000000000000000000001',
           'method': 'getDeepSecChkSwitch',
           'st': 'm',
           'chanid': 'guanwang',
           'sign': '',
           'bssid': '',
           'ssid': '' ,
           'mac':'d1:86:e3:6d:28:7c' }



dhid_param ={
        'capbssid': 'd8:86:e6:6f:a8:7c',
        'model': 'Nexus+4',
        'och': 'wandoujia',
        'appid': '0001',
        'mac': 'd1:86:e3:6d:28:7c',
        'wkver': '2.9.38',
        'lang': 'cn',
        'capbssid': 'test',
        'uhid': '',
        'st': 'm',
        'chanid': 'guanwang',
        'dhid': '',
        'os': 'android',
        'scrs': '768',
        'imei': '355136052321516',
        'manuf': 'LGE',
        'osvercd': '19',
        'ii': '355136052391516',
        'osver': '5.0.2',
        'pid': 'initdev:commonswitch',
        'misc': 'google/occam/mako:4.4.4/KTU84P/1227136:user/release-keys',
        'sign': '',
        'v': '58',
        'sim': '',
        'method': 'getTouristSwitch',
        'scrl': '1184'}


def get_pwd(ssids,bssids):
    params = pwd_params
    params['bssid'] = ','.join(bssids)
    params['ssid'] = ','.join(ssids)
    params['dhid'] = get_dhid()
    params['sign'] = sign(params)
    res = post(params)
    passwords = res.json().get('qryapwd',{}).get('psws',{})
    data = dict(zip(bssids,ssids))
    p_format = '{0:32} {1:32} {2:32}'
    print p_format.format('ssid','bssid','password')
    if passwords:
        for bssid in bssids:
            pwd = passwords.get(bssid.upper(),{}).get('pwd','')
            print p_format.format(data[bssid],bssid.upper(),decrypt_pwd(pwd) if decrypt_pwd(pwd) else '???????')


def get_dhid():
    params = dhid_param
    params['sign'] = sign(params)
    res = post(params)
    return res.json().get('initdev',{}).get('dhid','')

def post(params):
    url = 'http://wifiapi02.51y5.net/wifiapi/fa.cmd'
    headers = {
            'Content-type':'application/x-www-form-urlencoded',
            'Host':'wifiapi02.51y5.net'
            }
    return requests.post(url,headers=headers,params = params)

def sign(params):
    salt = 'LQ9$ne@gH*Jq%KOL'
    value = ''.join(OrderedDict(sorted(params.items())).values())+salt
    return hashlib.md5(value).hexdigest().upper()


def decrypt_pwd(password):
    if not password:
        return password
    key = "jh16@`~78vLsvpos"
    iv = "j#bd0@vp0sj!3jnv"
    cipher = AES.new(key = key, mode = AES.MODE_CBC, IV = iv )
    r = cipher.decrypt(password.decode('hex'))
    return r[3:][:int(r[0:3])]

def get_wifi_list():
    ignore_chars = '?#"\\'
    content = subprocess.check_output(['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport','-s'])
    result = {}
    for line in content.split('\n')[1:-1]:
        ssid,bssid = line.split()[0:2]
        if ':' in bssid and not(any(char in ssid for char in ignore_chars  )) :
            result[ssid] = bssid
    return result

def main():
    # get_dhid()
    # decrypt_pwd('B1B2699D2961C387A0C37E074158054A5AC5CC6AD716789D15A87E3FBB51D7C9')
    wifis = get_wifi_list()
    get_pwd(wifis.keys(),wifis.values())

if __name__ == '__main__':
    main()
