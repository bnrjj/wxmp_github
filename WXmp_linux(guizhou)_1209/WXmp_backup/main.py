# -*-coding: utf-8 -*-


from MpBot import Mpbot
from MpMsg import Mpmsg





if __name__ == '__main__':
    botobj = Mpbot()
    botwxobj = botobj.bot # 实例化发布者，在此具体就是实例化一个微信机器人
    regbot = Mpmsg(nummp=botobj.bot.mps(),numgp=botobj.bot.groups(),wxbot=botobj.bot)
    botobj.attach(regbot)
    #botobj.notify(regbot)
    pick = botobj.notify(regbot)
    pk = pickle.dumps(pick)
    p = Process(name=pk)
    p.start()


