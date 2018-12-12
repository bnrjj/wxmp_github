# /bin/python
# -*-coding: utf-8 -*-

from wxpy import *
from wxmpdata import print_mes

def mpupdate(mp,bot):
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

def main():
    bot = Bot(cache_path=True,console_qr=-2)
    mp = bot.mps()
    #lenmp = len(mp)
    mpupdate(mp,bot)

if __name__ == '__main__':
    main()


