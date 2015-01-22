#! /usr/bin/env python
#coding:utf8
from Crypto.Cipher import AES
import hashlib

article_key='AJ03lQmVmtomCfug'
product_key='XRbLEgrUCLHh94qG'
topic_key='36aAoQHCaJKETWHR'

BS=16

pad=lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-ord(s[-1])]

def encode_topic(topic_id):
    return aes_encript(topic_id,topic_key).strip()

def decode_topic(topic_id):
    return aes_decript(topic_id.decode('hex'),topic_key).strip()

def encode_product(product_id):
    return aes_encript(product_id,product_key).strip()

def decode_product(product_id):
    return aes_decript(product_id.decode('hex'),product_key).strip()

def encode_article(article_id):
    return aes_encript(article_id,article_key).strip()

def decode_article(article_id):
    return aes_decript(article_id.decode('hex'),article_key).strip()

def aes_encript(content,key):
    iv='1e5673b2572af26a8364a50af84c7d2a'.decode('hex')
    cipher=AES.new(hashlib.sha256(key).digest(),AES.MODE_CBC,iv)
    raw=pad(content)
    return cipher.encrypt(raw).encode('hex')

def aes_decript(content,key):
    iv='1e5673b2572af26a8364a50af84c7d2a'.decode('hex')
    cipher=AES.new(hashlib.sha256(key).digest(),AES.MODE_CBC,iv)
    return cipher.decrypt(content)


def main():
    #print encode_article('1440')
    #print decode_article(encode_article('1440'))
    #print encode_product('1234')
    #print decode_product(encode_product('1234'))
    #print decode_article('a630035c59ae23e156975ddbc5706a4a')
    print decode_topic(encode_topic('548223'))

if __name__ == '__main__':
    main()
