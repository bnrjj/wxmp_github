# -*-coding: utf-8 -*-
from mongoengine import *

connect('wxmp', host='localhost', port=27017)
#在所调用的函数里在函数体，即def...之前的语句在被调用时会执行，但只会执�?次，
# 这样就很有利于数据库mongodb或者连接kafka服务器这样的函数的使用，只会在第一次打开相应的网络ip地址�?
# 在之后的数据插入操作不会再重复的执行这个操作�?


class wxmpme(Document):
    Title = StringField(required=True)
    #Digest = StringField()
    Url = StringField(required=True)
    Content = ListField(required=True)
    PublishTime = StringField(required=True)
    #NickName = StringField(required=True)
    #Account = StringField(required=True)
    #Description = StringField(required=True)


    #以下为传入kafka的额外需添加的数�?
    from_type = IntField(required=True)
    resource = StringField(required=True)
    capture_time = StringField(required=True)


class wxmsg(Document):
    #name = StringField(required=True)
    ActualNickName = StringField(required=True)
    wx_Group = StringField(required=True)
    Text = StringField(required=True)
    CreateTime = IntField()

if __name__ == '__main__':
    u = 'http://mp.weixin.qq.com/s?__biz=MzI4NjAxMzM2Mg==&mid=602782654&idx=1&sn=ab41c692fb962e0a3b40651ad7b304fd&chksm=4dfa79637a8df07558a4fd77851201c9ee8d622749708228bae65e4e6b70ad60208bccf76107&scene=18#rd'
    aa = wxmpme.objects(Url=u)#.first()
    print aa.to_json()#无论是文档对象列表还是列表元素均可使用to_json()方法
    print type(aa.to_json())#json 类型就是str类型
    #print aa._query #相当于db.collections.find()
    #aa = wxmpme.objects(Url=u)[0] 或�?.first(),才能使用.to_mongo()方法，即改方法治适用与object文档对向列表的元�?
    #print aa.to_mongo()  #< class Bson>


