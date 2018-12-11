# -*-coding: utf-8 -*-


# 发布者的基类
class Subject(object):
    observer = []
    status = ""

    def attach(self,observer):
        pass

    def detach(self,observer):
        pass

    def notify(self,observer):
        pass


# 观察者的基类
class Observer(object):
    def __init__(self,nummp,numgp,wxbot):
        self.nummp = nummp
        self.wxbot = wxbot
        self.numgp = numgp

    def update(self):
        pass