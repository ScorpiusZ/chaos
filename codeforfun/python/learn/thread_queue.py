#! /usr/bin/env python
#coding:utf8
import threading
import time

class TaskManager(threading.Thread):
    queue=[]
    def addTask(self,url):
        self.queue.append(url)
        print 'addTask %s'%url

    def run(self):
        print 'task is running'
        while len(self.queue):
            print self.queue[0]
            self.queue=self.queue[1:]
            time.sleep(0.1)


def demo():
    taskManager=TaskManager()
    for i in xrange(5):
        url='this is a url %d'%i
        taskManager.addTask(url)
        if not taskManager.isAlive():
            taskManager.start()

    for i in xrange(5,10):
        url='this is a url %d'%i
        taskManager.addTask(url)
        if not taskManager.isAlive():
            taskManager.start()



def main():
    demo()

if __name__ == '__main__':
    main()
