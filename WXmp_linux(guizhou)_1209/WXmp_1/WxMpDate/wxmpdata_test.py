# /bin/python
# -*-coding: utf-8 -*-

import time
# from pymongo import MongoClient
import xml.etree.ElementTree as ETree

from wxpy import *

# from datetime import *
from captureTime import capture_time
#from WxMpDate.captureTime import capture_time
from mpcrawl import MpCrawl
from wxmpME import wxmpme,wxmsg
from kafka import KafkaProducer
from connectkafka import connect_kafka
import json
#import logging as log
#log.basicConfig(level=log.DEBUG,filename='wxmp_log.log',filemode='a',format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

'''
import logging as log
from logging import handlers
LOG_FILE = 'wxmp_log.log'
handler = log.handlers.TimedRotatingFileHandler(LOG_FILE, when='h', interval=24, backupCount=3)
fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = log.Formatter(fmt)
handler.setFormatter(formatter)
logger = log.getLogger('wxmp_log')
logger.addHandler(handler)
logger.setLevel(log.DEBUG)
log.basicConfig(level=log.DEBUG,filename='wxmp_log.log',filemode='a',format=fmt)
'''
from wx_log import WX_log

wxmp_log = WX_log()

def find_text(item,tag):
    found = item.find(tag)
    if found is not None:
                # print found.text
    	return found.text



def print_mes(msg):
    art = msg.raw.get('Content')
    art1 = art.encode('utf-8')# 需要将msg.raw.get（）这个方法值进行utf-8的编码，才能作为ETree的输�?
    # print type(art1)
    # print art1
    tree = ETree.fromstring(art1)
    #print type(tree)
    #print tree
    items = tree.findall('.//mmreader/category/item')
    print items
    wxmp_log.mylog(items)
    article_list = list()

    for item in items:

        article = Article()
        article.title = find_text(item,'title')
	wxmp_log.mylog(article.title)
        #print article.title
        article.summary = find_text(item,'digest')
        #print  article.summary
        article.url = find_text(item,'url')
	wxmp_log.mylog(article.url)
	
        article.pub_time = find_text(item,'pub_time')#�?unix�?时间戳转换为公元时�?
        #print type(article.pub_time)
        localtime = int(article.pub_time)
        pubtime = time.localtime(localtime)
        otherpubtime = time.strftime("%Y-%m-%d", pubtime)
        print otherpubtime
        #print pubtime
        #url = MpCrawl(article.url)

	ti = 0
        url = MpCrawl(article.url)
        while ti <= 5:
            if url.mphtml is not None:
	    #if isinstance(url.mphtml,instance):
                break
            else:
                url = MpCrawl(article.url)
                ti += 1
                time.sleep(10)
                print "this is the No %s" %ti
		wxmp_log.mylog("this is the No %s" %ti)
 
        urlparse = url.parse()
        mxcontent = list(urlparse)
	#print mxcontent
        #nickname = url.mpnickname()
        #account = url.mpnumber()
        #description = url.mpfun()
        #print mxcontent
	#wxmp_log.mylog(article.url)
        print 'this is mes:',article.url
        article.cover = find_text(item,'cover')

        wxmpmsg = wxmpme(
            Title=article.title,
            #Digest=article.summary,
            Url=article.url,
            Content=mxcontent,
            PublishTime=otherpubtime,
            #NickName=nickname,
            #Account=account,
            #Description=description
            from_type=19,
            resource='weixin',
            capture_time=capture_time()
        )
	wxmpmsg.save()
        

        #mongodata = wxmpme.objects(Url=article.url)[0].to_mongo()#.to_json()
        # #将每条公众号对应mongo的数据经过to_mongo()方法转化成Bson格式（是json的一种二进制存储格式）的数据，方便kafka的传�?
        # 但是to_mongo()只能对mongo objects对象列表中的一个元素进行格式转化，而to_json()则可对对象列表进行全部的转化

        mongodata = wxmpme.objects(Url=article.url).order_by('-capture_time')[0].to_json() #使用json格转化数据式
        #print mongodata
	jsondata = {
            'Title':article.title,
            'Url':article.url,
            'Content':mxcontent,
            'PublishTime':otherpubtime,
            'from_type':19,
            'resource':'weixin',
            'capture_time':capture_time()
        }

	connect_kafka(mongodata)
	#wxmp_log.mylog()
    #return mongodata
        

        #producer = KafkaProducer(bootstrap_servers='10.61.120.136:9092')
        #producer.send('weixin',b'a test')

def print_gpmsg(ms):
    print ms.raw.get('ActualNickName')
    print ms.raw.get('Text')
    group = str(ms.sender)
    ms.raw['wx_Group'] = group
    msg = wxmsg(
        ActualNickName=ms.raw.get('ActualNickName'),
        Text=ms.raw.get('Text'),
        wx_Group=ms.raw.get('wx_Group'),
        CreateTime=ms.raw.get('CreateTime')
        )
    # = bot.groups()
    #print mf2
    msg.save()

def mpupdate(mp):
    lenmp = len(mp)
    print lenmp

    @bot.register(chats=mp, except_self=False)
    def waibufun(ms):
        print_mes(ms)
        #print len(mpup)
        #print ms.raw
        #return  len(mpup)
        mpup = bot.mps(update=True)
        print len(mpup)
        if lenmp != len(mpup):
            #mpp = bot.mps(update=True)
            mpupdate(mpup)
    embed()


# g = u'五星体育'
if __name__ == '__main__':
    bot = Bot(cache_path=True,console_qr=-2)
    mp = bot.mps()
    #lenmp = len(mp)
    mpupdate(mp)



'''    
    if msg.type == SHARING and isinstance(msg.sender, MP):
        print 'hh'
        tree = ETree.fromstring(msg.raw['Content'])
        print 'hhh'
        items = tree.findall('.//mmreader/category/item')

        article_list = list()

        for item in items:
            def find_text(tag):
                found = item.find(tag)
                if found is not None:
                    return found.text

            article = Article()
            article.title = find_text('title')
            article.summary = find_text('digest')
            article.url = find_text('url')
            article.cover = find_text('cover')
            article_list.append(article)

        return article_list


embed()
'''