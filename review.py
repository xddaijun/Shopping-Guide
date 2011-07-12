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

conn =MySQLdb.Connection(host='127.0.0.1', user='root', passwd='mysql', db='shopping',use_unicode=1, charset='utf8')

errorid=0          

def getUrlFromDatabase(ptype):
    global errorid
    typeeunm={"手机":'phone_nphone',"相机":'digital_ncamera',"笔记本":'digital_ndigital'}
    if ptype in typeeunm.keys():
        cur=conn.cursor()
        cur.execute("select id,curl,name from %s;" % typeeunm[ptype])      
        rows=cur.fetchall()
        cur.close()
        for r in rows:
            try:
                otable={}
                otable['name']=r[2]
                otable['url']=r[1]
                otable['pid']=str(r[0])
                otable['ptype']=ptype
                otable['savedate']=str(datetime.datetime.now())
                otable['sources']=u'ZOL中关村在线'
                if otable['url'].find("None")<0:
                    while True:
                        m=getReview(otable)
                        if m:
                            otable['url']=m
                        else:
                            break
            except Exception, what:
                errorid+=1        
                print "expetion%d" % errorid  
                print what  
                print otable['url']
                continue                
                
            
def getReview(otable):
    global errorid
    cur =conn.cursor()
    res = urllib2.urlopen(otable['url'],None,60) # timeout=60s
    html = res.read()            
    s=BeautifulSoup(unicode(html,"gbk"))       
    for liurl in s.findAll('div',attrs={'class':'c'}):
        try:                     
            otable['title']=liurl.find('div',attrs={'class':'ltit '}).getText()
            otable['advantage']=liurl('dd')[0].getText()
            otable['shortcoming']=liurl('dd')[1].getText()
            otable['summarize']=liurl('dd')[2].getText()
            otable['score']=liurl.find('b',attrs={'class':'lv'}).getText()[0:1]            
            isT=int(liurl.find('span',attrs={'id':re.compile('goodnum_')}).getText())
            isF=int(liurl.find('span',attrs={'id':re.compile('badnum_')}).getText())
            if(isT+isF<10):
                otable['credibility']="0.8"
            else:
                otable['credibility']="%f"%(isF/(isT+isF)*1.0)
            otable['username']=liurl.find('a',attrs={'href':re.compile('http://my.zol.com.cn')}).getText()
            
            otablesKeys=','.join(otable.keys())
            otablesValues='"'+'","'.join(otable.values())+'"'
            inssql='insert into  digital_review(%s)  values(%s)'%(otablesKeys,otablesValues)
            print inssql                
            cur.execute(inssql)
        except Exception, what:
            errorid+=1        
            print "expetion%d" % errorid  
            print what             
            continue   
            
    cur.close()
    if len(s.findAll('span',attrs={'class':'next'}))>0:
        m='http://detail.zol.com.cn'
        m+=s.findAll('span',attrs={'class':'next'})[0].previous['href']
        return m
    return None
    
    
def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    getUrlFromDatabase("手机")
    getUrlFromDatabase("相机")
    getUrlFromDatabase("笔记本")
    #otable= getfromZolSpec('http://detail.zol.com.cn/290/289513/param.shtml')
    #for v in otable.keys():
    #    print v,otable[v]
    #for ix in range(1,189):
    #    getfromZol(ix)

    #getfromSOSO
    #print outstr[0]
     


if __name__ == '__main__':
    start = time.clock()
    main()
    end = time.clock()
    print 'use time :%f' % (end-start)