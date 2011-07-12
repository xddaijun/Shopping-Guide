# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 13:30:05 2011

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
import socket

socket.setdefaulttimeout(10) 

conn =MySQLdb.Connection(host='127.0.0.1', user='root', passwd='tcna2005', db='shopping',use_unicode=1, charset='utf8')

errorid=0 

def getYoudao(ptype):    
    global errorid
    alltype={"phone":('phone_nphone',urllib2.quote('手机')),  
             "camera":('digital_ncamera',urllib2.quote('数码相机')),  
            "digital":('digital_ndigital',urllib2.quote('笔记本电脑'))}
    headers = {
    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    }
    
    if ptype in alltype.keys():
        cur=conn.cursor()
	if ptype=='digital':
            cur.execute("select id,name from %s where id>169;" % alltype[ptype][0])      
	else:
            cur.execute("select id,name from %s;" % alltype[ptype][0])      
        rows=cur.fetchall()
        cur.close()
        cur =conn.cursor()
        for r in rows:
            pname=r[1]
            pid=r[0]
            otable={}
            otable['pid']=str(pid)
            otable['ptype']=ptype
            otable['name']=pname
            pname=re.sub(u'（[^（）]+）',' ',pname)
            #encodedQuery = pname.decode("utf-8").encode("gbk") 
            fullUrl = r'http://gouwu.youdao.com/detail?q=%s&sub_cat=%s&ue=utf-8&tab=PRICE_TAG' \
            % (urllib2.quote(pname.encode("utf-8")),alltype[ptype][1])
            try:                
                req = urllib2.Request(url = fullUrl,headers = headers)
                proxy_support = urllib2.ProxyHandler({'http':'http://219.137.229.210:3128'})#
                opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
                urllib2.install_opener(opener)
                res = urllib2.urlopen(req)
                html = res.read()
                time.sleep(5) # don't spam                
                s=BeautifulSoup(html)
                tds=s.findAll('tr',attrs={'class':'  '})
                for tr in tds:
                    otable['sname']=tr('h3',attrs={'class':'goods-name'})[0]('a')[0]['data-site']
                    otable['spname']=tr('h3',attrs={'class':'goods-name'})[0]('a')[0].getText()
                    otable['surl']=tr('h3',attrs={'class':'goods-name'})[0]('a')[0]['data-orgurl']
                    otable['price']=tr('em',attrs={'class':'asynprice'})[0].getText()
                    otable['savedate']=str(datetime.datetime.now())
                    otablesKeys=','.join(otable.keys())
                    otablesValues='"'+'","'.join(otable.values())+'"'
                    inssql='insert into  digital_price(%s)  values(%s)'%(otablesKeys,otablesValues)
                    #print inssql   
                    cur.execute(inssql)                    
            except Exception, what:
                errorid+=1        
                print "expetion%d" % errorid  
                print what
                continue
        cur.close()
    
def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    #getYoudao("phone")
    #getYoudao("camera")
    getYoudao("digital")
     


if __name__ == '__main__':
    start = time.clock()
    main()
    end = time.clock()
    print 'use time :%f' % (end-start)
