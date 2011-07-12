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

conn =MySQLdb.Connection(host='127.0.0.1', user='root', passwd='mysql', db='shopping',use_unicode=1, charset='utf8')

errorid=0 

def getYoudao(ptype):    
    global errorid
    alltype={"phone":('phone_nphone',urllib2.quote('手机')),  
             "camera":('digital_ncamera',urllib2.quote('数码相机')),  
            "digital":('digital_ndigital',urllib2.quote('笔记本电脑'))}

    if ptype in alltype.keys():
        cur=conn.cursor()
        cur.execute("select id,name from %s;" % alltype[ptype][0])      
        rows=cur.fetchall()
        cur.close()
        for r in rows:
            pname=r[1]
            pid=r[0]
            pname=re.sub(u'（[^（）]+）',' ',pname)
            #encodedQuery = pname.decode("utf-8").encode("gbk") 
            fullUrl = r'http://gouwu.youdao.com/detail?q=%s&sub_cat=%s&ue=utf-8#tab%3DPRICE_TAG' \
            % (urllib2.quote(pname),alltype[ptype][1])
            try:
                res = urllib2.urlopen(fullUrl,None,60)
                html = res.read()
                s=BeautifulSoup(html)
            except Exception, what:
                errorid+=1        
                print "expetion%d" % errorid  
                print what
                continue
    
def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    #getfromEtaoSpec('http://s.etao.com/search?q=%CA%D6%BB%FA&epid=2163041&v=product&p=detail&cat=1512&position=6&from=list-price-NULL-grid')
    for s in range(0,73*40,40):
        getfromEtao("手机",s)
    g.close()
    #getfromSOSO
    #print outstr[0]
     


if __name__ == '__main__':
    start = time.clock()
    main()
    end = time.clock()
    print 'use time :%f' % (end-start)