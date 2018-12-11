# -*-coding: utf-8 -*-

from wxpy import *
from WxmpObserver import Subject


class Mpbot(Subject):
    def __init__(self):
        self.bot = Bot(cache_path=True,console_qr=-2) #Mpbot的初始化属�?bot是wxpy的Bot�?
        self.mp = self.bot.mps(update=True)
        self.group = self.bot.groups(update=True)
        #self.listlen = len(self.bot.mps(update=True))

    def attach(self, obser):
        self.observer.append(obser)
        #return obser

    def detach(self, obser):
        self.observer.remove(obser)
        #return obser

    def notify(self, obser):
        for obser in self.observer:
            obser.update()
        #obser.update()

'''
exbot = Mpbot()
a = exbot.bot
print type(a)
b = exbot.listlen
print b



while True:
    @exbot.register(chats=mp)
    def exzample(msg):
        print "kakaka"
        a = msg.raw.get('Content')
        print a

    mp = exbot.mps(update=True)
    print len(mp)
'''