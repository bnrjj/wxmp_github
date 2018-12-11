# -*-coding: utf-8 -*-
from WxmpObserver import Observer
from WxMpDate import wxmpdata
from MpBot import Mpbot
from wxpy import *
#import xml.etree.ElementTree as ETree
#from MpBot import *


class Mpmsg(Observer):
    def update(self):
        @self.wxbot.register(chats=self.nummp)#(chats=[Group,MP])
        def mpmsg(msg):
            #if isinstance(msg.chat,Group):           
            #	wxmpdata.print_gpmsg(msg)
	    #else:
            wxmpdata.print_mes(msg)
            #self.numgp = Mpbot().bot.groups(update=True)
	    self.nummp = Mpbot().bot.mps(update=True)
        #embed()
        self.wxbot.join()


