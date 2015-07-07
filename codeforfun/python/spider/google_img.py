#! /usr/bin/env python
#coding:utf8
import urllib
import requests
import time


def find(keywords):
    url='https://ajax.googleapis.com/ajax/services/search/images?v=1.0&rsz=8&q='
    querry='+'.join(urlEncode(keywords))
    url=url+querry
    search4Result(url,64)

def urlEncode(keywords):
    res=[]
    for word in keywords:
        res.append(urllib.quote_plus(word))
    return res

def search4Result(url,count):
    per_count=8
    i=0
    url=url+'&start={}'
    while count>0:
        try:
            requesturl=url.format(str(i*per_count))
            print
            print requesturl
            print
            response=requests.get(requesturl,timeout=10)
            content=response.json()
            for img in content['responseData']['results']:
                imgurl=img['url']
                imgurl=str(imgurl)
                print imgurl
                if imgurl:
                    download_file(img['url'])
            count=count-per_count
            i=i+1
        except :
            time.sleep(20)
            count=count-per_count
            i=i+1
            continue

def download_file(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    local_filename=img_dir()+'/'+str(int(round(time.time()*1000)))+'_'+local_filename
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
    return local_filename

def img_dir():
    import os
    cur_dir=os.path.dirname(os.path.abspath(__file__))
    imgs_dir=cur_dir+os.path.sep+'imgs'
    if not os.path.exists(imgs_dir):
        os.mkdir(imgs_dir)
    return imgs_dir

def main():
    find(['美女交友','banner'])
    #find(['美女诱惑','banner'])
    #find(['美女游戏','banner'])
    #find(['交友诱惑','banner'])

if __name__ == '__main__':
    main()
