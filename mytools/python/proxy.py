#! /usr/bin/env python
#coding:utf8
from twisted.web import proxy, http
from twisted.internet import reactor
from twisted.python import log
import sys
log.startLogging(sys.stdout)

if len(sys.argv)>1:
    port=int(sys.argv[1])
else:
    port=8080


class ProxyFactory(http.HTTPFactory):
    protocol = proxy.Proxy

reactor.listenTCP(port, ProxyFactory())
reactor.run()
