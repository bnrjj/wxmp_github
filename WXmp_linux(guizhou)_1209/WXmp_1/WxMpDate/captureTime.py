# /bin/python
# -*-coding: utf-8 -*-
from datetime import * #在time模块后再加入datetime模块 之前的time函数会出现错�?
#import datetime


def capture_time():

    #print datetime.now()
    t = datetime.now()
    at = t + timedelta(hours=-8)
    #return str(datetime.now())
    #print '%s'% t.isoformat()
    tt = datetime.strftime(at,'%Y-%m-%dT%H:%M:%S%zZ')
    return tt
    #return datetime.strftime(datetime.now(),'%Y-%Z')
if __name__=='__main__':
    print capture_time()