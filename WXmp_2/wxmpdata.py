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
       return found.text

def print_mes(msg):
    art = msg.raw.get('Content')
    art1 = art.encode('utf-8')# éœ€è¦å°†msg.raw.getï¼ˆï¼‰è¿™ä¸ªæ–¹æ³•å€¼è¿›è¡Œutf-8çš„ç¼–ç ï¼Œæ‰èƒ½ä½œä¸ºETreeçš„è¾“ï¿?
    tree = ETree.fromstring(art1)
    items = tree.findall('.//mmreader/category/item')
    print items
    wxmp_log.mylog(items)
    article_list = list()

    for item in items:
        article = Article()
        article.title = find_text(item,'title')
	wxmp_log.mylog(article.title)
        article.summary = find_text(item,'digest')
        article.url = find_text(item,'url')
	wxmp_log.mylog(article.url)
        article.pub_time = find_text(item,'pub_time')#å°?unixçš?æ—¶é—´æˆ³è½¬æ¢ä¸ºå…¬å…ƒæ—¶ï?
        localtime = int(article.pub_time)
        pubtime = time.localtime(localtime)
        otherpubtime = time.strftime("%Y-%m-%d", pubtime)
        print otherpubtime
	ti = 0
        url = MpCrawl(article.url)
        while ti <= 5:
            if url.mphtml is not None:
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
        # #å°†æ¯æ¡å…¬ä¼—å·å¯¹åº”mongoçš„æ•°æ®ç»è¿‡to_mongo()æ–¹æ³•è½¬åŒ–æˆBsonæ ¼å¼ï¼ˆæ˜¯jsonçš„ä¸€ç§äºŒè¿›åˆ¶å­˜å‚¨æ ¼å¼ï¼‰çš„æ•°æ®ï¼Œæ–¹ä¾¿kafkaçš„ä¼ ï¿?
        # ä½†æ˜¯to_mongo()åªèƒ½å¯¹mongo objectså¯¹è±¡åˆ—è¡¨ä¸­çš„ä¸€ä¸ªå…ƒç´ è¿›è¡Œæ ¼å¼è½¬åŒ–ï¼Œè€Œto_json()åˆ™å¯å¯¹å¯¹è±¡åˆ—è¡¨è¿›è¡Œå…¨éƒ¨çš„è½¬åŒ–

        mongodata = wxmpme.objects(Url=article.url).order_by('-capture_time')[0].to_json() #ä½¿ç”¨jsonæ ¼è½¬åŒ–æ•°æ®å¼
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
