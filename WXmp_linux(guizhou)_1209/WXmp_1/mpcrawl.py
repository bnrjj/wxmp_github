# /bin/python
#  -*-coding: utf-8 -*-
from urllib2 import urlopen, URLError,Request
from bs4 import BeautifulSoup as BS
from pymongo import MongoClient
from wx_log import WX_log
wxmp_log = WX_log()

def openwxurl(url):
    user_agent ='Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'
    hearders = {'User-Agent':user_agent}
    req = Request(url=url,headers=hearders)
    response = urlopen(req)
    return response


class MpCrawl(object):
    def __init__(self, mp_url):
        self.mp_url = mp_url
        print 'this is spider:',self.mp_url
        
	try:
	    #self.mphtml = urlopen(self.mp_url,timeout=60)
	    self.mphtml = openwxurl(self.mp_url)
	    print self.mphtml
	except URLError as e:
	    if hasattr(e,'reason'):
                wxmp_log.mylog('reason:', e.reason)
	    elif hasattr(e,'code'):
	        wxmp_log.mylog('Error code', e.code)
	else:
	    wxmp_log.mylog('already open the url')
            self.mpbso = BS(self.mphtml, 'lxml')


    def parse(self):
        #mphtml = urlopen(self.mp_url)
        #mpbso = BS(mphtml, 'lxml')
        mpcontent = self.mpbso.find('div', {'id': 'js_content'}).get_text()#.findAll({'section', 'p'})
        wxmp_log.mylog('parse the content')
        yield mpcontent
        #print type(mpcontent)
        #mpcontentlist =  list(mpcontent)
        #for i in mpcontent:
            #print i
            #content = i.get_text().strip()
            #content = i.get_text()
            #print content
            #if content is not u'':
                #yield content
                #print content

    def mpnickname(self):
        nickname = self.mpbso.find('div', {'class': 'profile_inner'}).find(attrs={'class': 'profile_nickname'})
        #print type(nickname.get_text())
        return nickname.get_text()
        #nickname = nickname.get_text()
        #print nickname
        #return nickname

    #def mpnumber(self):
        #num = self.mpbso.find('label', text=u'微信�?).next_siblings # num的类型是生成器（generator），该类型的数据是不保存在内存中的，因此当第一次调用之后再次调用就不是空�?
        #print type(num)
        #print list(num)
        #print list(num)
        #number = list(num)
        #print type(number)
        #print len(number)
        #print number
        #print number[1]#.get_text()
        #return number
        #return list(num)[1].get_text()
	#pass

    #def mpfun(self):
        #fun = self.mpbso.find('label', text=u'功能介绍').next_siblings
        #return list(fun)[1].get_text()
	#pass

    #def publishtime(self):
    #    pubtime = self.mpbso.find(attrs={'id': 'publish_time'})#.get_text()
     #   return pubtime

if __name__ == '__main__':
    client = MongoClient('localhost', 27017)
    db = client.test
    a = "https://mp.weixin.qq.com/s?__biz=MzU1NDA4NjU2MA==&mid=2247492243&idx=2&sn=71eb938ea6ff144fe25846c0773a9854&chksm=fbea5b5ccc9dd24ae2cefaafb2212487f8b28668624890f2de043908b69f09cdd07c03d94ef8&scene=0#rd"
    aa = MpCrawl(a)
    wxcontent = aa.parse()
    print wxcontent
    nick = aa.mpnickname()
    num = aa.mpnumber()
    fun = aa.mpfun()
    #pubtime = aa.publishtime()
    #print pubtime


    db.text.insert(
        {"title": "this is a text of wxmp_content_17",
        "content": list(wxcontent),
        "nick": nick,
        "num": num,
        "fun": fun,
         #"publishtime":pubtime
        }
    )


'''
        mpnickname = mpbso.find('div', {'class': 'profile_inner'}).find(attrs={'class': 'profile_nickname'})
        nickname = mpnickname.get_text()
        print nickname
        #print type(mpnickname)
        #最低要求：仅仅获取该公众号的number
        #mpmetadata = mpbso.find('p', {'class': 'profile_meta'})
        #wxmpname = mpmetadata.find('span', {'class': 'profile_meta_value'}).get_text()
        #print wxmpname

        #基本要求：获取该公众号的number以及公众号描述信�?
        mpmetadata = mpbso.find('label', text=u'微信�?) # <label class="profile_meta_label">微信�?/label>
        wxmpname = mpmetadata.next_siblings  # 1.我不知道next_sibling是用来干什么的，他什么都不能�?
        for i in wxmpname:                  # 2.只能用next_siblings来提取当前标�?'label', text=u'微信�?)的邻居�?��?
            print i.string                  # 3.next_siblings返回的是一个生成器，该迭代以后的对象是“Navigable String”对象，需要用.string来提取里面文本内�?

        mpmetadata = mpbso.find('label', text=u'功能介绍')
        wxmpdis = mpmetadata.next_siblings
        for i in wxmpdis:
            print i.string
        #发布时间无�?�获取？？�?
        #mppublisdate = mpbso.find('em', {'id':'publish_time'})
        #print mppublisdate
'''

'''def mpnumber(self):
        #num = self.mpbso.find('label', text=u'微信�?).next_siblings
        #yield num       
        for number in self.mpbso.find('label', text=u'微信�?).next_siblings:
            num = unicode(number.string)
            print num
            #if num is not u'\n':
            #print number.string
            #print type(number.string)
            return number.string
'''


'''
content = mpcontent[0].get_text()
        print content
        print type(content)
        a =u''
        print type(a)
'''
'''            print content
            db.wxx.update(
                {"name": u"今夏最想念的味道，是什么？"},
                {"$push": {"content": content}}

            )

'''










# aaa = "hahahaha"
# uri = MpCrawler(aaa)
# uri.__init__(aaa)
