# /bin/python
#  -*-coding: utf-8 -*-

from kafka import KafkaProducer
import json
#import logging as log
#log.basicConfig(level=log.DEBUG)

producer = KafkaProducer(bootstrap_servers='10.61.120.136:9092')
#producer = KafkaProducer(bootstrap_servers='10.61.120.136:9092',value_serializer=lambda v: json.dumps(v).decode('utf-8').replace(r'\\u','\u'))

def connect_kafka(mongodate):
    
    producer.send('weixin', mongodate)
    #print mongodate

#for _ in range(10):
#    producer.send('weixin',b'This is a test')
'''

#from pykafka import KafkaClient
# from kafka import KafkaProducer

import json
import logging
import time
import sys


#host='10.61.120.136:9092'
#client = KafkaClient(hosts=host)
#topic = client.topics[b'weixin']
#p = topic.get_producer()
#p.start()
#p.produce('test')
#p.stop()
#print client.topics
#print("135")
#topic = client.topics[b'weixin']
'''

'''producer = topic.get_producer()
producer.start()

# 生产消息
msg_dict = {
    "sleep_time": 10,
    "db_config": {
        "database": "test",
        "host": "192.168.137.12",
        "user": "root",
        "password": "root"
    },
    "table": "msg",
    "msg": "Hello World"
}
msg = json.dumps(msg_dict)
msg=bytes(msg)
for i in range(100):
    producer.produce(msg)
producer.stop()
'''