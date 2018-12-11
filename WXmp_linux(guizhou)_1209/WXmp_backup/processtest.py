# -*-coding: utf-8 -*-
from multiprocessing import Process
from MpBot import Mpbot
from MpMsg import Mpmsg
n=100 #在windows系统中应该把全局变量定义在if __name__ == '__main__'之上就可以了
def work():
    global n
    n=0
    print( 'zijincheng',n)


if __name__ == '__main__':
    #p=Process(target=work)
    #p.start()
    botobj = Mpbot()
    regbot = Mpmsg(nummp=botobj.bot.mps(),wxbot=botobj)
    botobj.attach(regbot)

    p1 = Process(target=botobj.notify, args=(regbot,))
    p1.start()
    p1.join()
    print('hkaka ',n)