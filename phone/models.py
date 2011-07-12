# -*- coding: utf-8 -*-

from django.db import models


class Phone(models.Model):
    name=models.CharField(u'名称',max_length=128,null=True)
    url = models.URLField(u'抓取地址',max_length=255, unique=True)  
    price=models.CharField(u'价格',max_length=30,null=True)
    savedate = models.DateTimeField(u'保存时间',auto_now_add=True,blank=True,null=True)  
    img = models.ImageField(u'图片地址',upload_to = 'nphone')
    screensize=models.CharField(u'主屏尺寸',max_length=128,null=True)
    screencolors=models.CharField(u'屏幕颜色',max_length=128,null=True)
    stroage=models.CharField(u'存储功能',max_length=128,null=True)
    ringing=models.CharField(u'铃声',max_length=128,null=True)
    markettime=models.CharField(u'上市时间',max_length=128,null=True)
    modletype=models.CharField(u'型号',max_length=128,null=True)
    system=models.CharField(u'操作系统',max_length=128,null=True)
    issmart=models.CharField(u'是否智能机',max_length=128,null=True)
    camera=models.CharField(u'摄像头',max_length=128,null=True)
    brand=models.CharField(u'品牌',max_length=128,null=True)
    outward=models.CharField(u'外观',max_length=128,null=True)

class NPhone(models.Model):
    name=models.CharField(u'名称',max_length=128,null=True)
    url = models.URLField(u'抓取地址',max_length=255, unique=True)  
    curl = models.URLField(u'评论地址',max_length=255, null=True) 
    price=models.CharField(u'价格',max_length=30,null=True)
    savedate = models.DateTimeField(u'保存时间',auto_now_add=True,blank=True,null=True)  
    img = models.ImageField(u'图片地址',upload_to = 'phone')
    screensize=models.CharField(u'主屏尺寸',max_length=128,null=True)
    screencolors=models.CharField(u'屏幕颜色',max_length=128,null=True)   
    markettime=models.CharField(u'上市时间',max_length=128,null=True)    
    system=models.CharField(u'操作系统',max_length=128,null=True)    
    camera=models.CharField(u'摄像头',max_length=128,null=True)    
    outward=models.CharField(u'外观',max_length=128,null=True)
    def __unicode__(self):  
        return "%s"%self.name
