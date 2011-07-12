# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 19:10:01 2011

@author: mark
"""
import re
import sys
import time
import urllib2
from BeautifulSoup import *
import MySQLdb
import datetime
import os
g=open('digital.txt','w')
image_path=os.path.join(os.path.dirname(__file__), 'digital/').replace('\\','/')
conn =MySQLdb.Connection(host='127.0.0.1', user='root', passwd='mysql', db='shopping',use_unicode=1, charset='utf8')
phoneenum={u'处理器型号':'processor',u'处理器主频':'frequency', 
           u'内存容量':'storage',u'硬盘容量':'harddrive', 
           u'屏幕尺寸':'screensize',u'显卡芯片':'Graphics',
           u'上市日期':'markettime',u'操作系统':'system',
           u'笔记本重量':'weight'}
errorid=0          
html_image=''       
def getfromZol(page):    
    global errorid
    fullUrl = r'http://detail.zol.com.cn/notebook_index/subcate16_0_list_1_0_1_1_1_%d.html'%page
    res = urllib2.urlopen(fullUrl,None,60) # timeout=60s
    html = res.read()

    s=BeautifulSoup(unicode(html,"gbk"))    
    for liurl in s.findAll('div',attrs={'class':'item'}):
        try:        
            name=liurl.find('a',attrs={'class':'title'}).getText()#name
            url=liurl('a',href=re.compile('.*param.shtml'))[0]['href']#参数URL
            if(len(liurl('a',href=re.compile('.*review.shtml')))>0):
                curl=liurl('a',href=re.compile('.*review.shtml'))[0]['href']#点评URL
                curl='http://detail.zol.com.cn'+curl
            else:
                curl="None"
            price=liurl.find('span',attrs={'class':'price'})('b')[0].getText()  
            url='http://detail.zol.com.cn'+url
                  
            img=liurl.find('a',attrs={'class':'hidden'}).getText().replace('80x60','280x210')
            otable=getfromZolSpec(url)
           
            otable['name']=name
            otable['url']=url
            otable['curl']=curl
            otable['price']=price
            otable['savedate']=str(datetime.datetime.now())
            
            
            imagedata = urllib2.urlopen(img).read()  
            image = "ndigital/%s%d.jpg"%(''.join(re.findall('\w+',name)),int(time.time()))  
            f = file(image_path+image,'wb')  
            f.write(imagedata)  
            f.close()  
            otable['img']=image
            
            cur =conn.cursor()
            otablesKeys=','.join(otable.keys())
            otablesValues='"'+'","'.join(otable.values())+'"'
            inssql='insert into  digital_ndigital(%s)  values(%s)'%(otablesKeys,otablesValues)
            print inssql 
            cur.execute(inssql)            
            print>>g,("%s\t\t%s")%(name,price) 
        except Exception, what:
            errorid+=1        
            print "expetion%d" % errorid  
            print what           
            continue

def getfromZolSpec(fullUrl):
    otable={}
    res = urllib2.urlopen(fullUrl,None,60) # timeout=60s
    html = res.read()
    s=BeautifulSoup(unicode(html,"gbk"))
    tds=s.find('table',attrs={'id':'param-tb'})('td')
    for itd in range(len(tds)):
        td=tds[itd]
        if td.getText() in phoneenum.keys():
            otable[phoneenum[td.getText()]]=tds[itd+1].getText().replace(u"纠错","")
    
    return otable
        
    
def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    #otable= getfromZolSpec('http://detail.zol.com.cn/290/289513/param.shtml')
    #for v in otable.keys():
    #    print v,otable[v]
    #for ix in range(1,174):
    getfromZol(6)
    g.close()
    #getfromSOSO
    #print outstr[0]
     


if __name__ == '__main__':
    start = time.clock()
    main()
    end = time.clock()
    print 'use time :%f' % (end-start)