# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 22:43:10 2011

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

conn =MySQLdb.Connection(host='127.0.0.1', user='root', passwd='tcna2005', db='shopping',use_unicode=1, charset='utf8')
oridict={}
desdict={}
allwnums=0
def bayQuery(ptype):  
    alltype={"phone":'phone_nphone',"camera":'digital_ncamera',"digital":'digital_ndigital'}
    global oridict,desdict,allwnums
    if ptype in alltype.keys():
        cur=conn.cursor()
        cur.execute("select id,name from %s;" % alltype[ptype])      
        rows=cur.fetchall()
        cur.close()
        for r in rows:
            oridict[r[0]]=r[1]
            for w in segQuery(r[1]):
                if w  not in desdict.keys():
                    desdict[w]=[]
                desdict[w].append(r[0])
        for d in desdict.keys():
            allwnums+=len(desdict[d])
            
 
def getid(word):
    global oridict,desdict
    words=segQuery(word)
    score=0.0
    outres=[]
    for w in words:
        if w in desdict.keys():
            outres.append(desdict[w])
    if len(outres)>=1:
        outres.sort(key=len)
    for ix in range(1,len(outres)):
        ll=list(set(outres[0]).intersection(set(outres[ix])))
        if len(ll)>0:
            return ll[0],oridict[ll[0]]
            #score+=allwnums/len(desdict[w])
            #if len(desdict[w])==1:
            #    print w,len(desdict[w])
            #    return (desdict[w][0],oridict[desdict[w][0]])
    return score
    #print score
               
        
def segQuery(word):
    word=re.sub(u'（[^（）]+）',' ',word)
    for s in [u'）','（','/']:
        word=word.replace(s,' ')
    chinese=re.findall('[^\w\s-]+',word)
    english=re.findall('[\w-]+',word)
    chinese.extend(english)
    return chinese

def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    print segQuery(u"诺基亚（NOKIA）E63 3G手机（黑色）WCDMA/GSM 非定制机")
    bayQuery("phone")
    print getid(u"诺基亚（NOKIA）E63 3G手机（黑色）WCDMA/GSM 非定制机")



if __name__ == '__main__':
    start = time.clock()
    main()
    end = time.clock()
    print 'use time :%f' % (end-start)
    