# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class NDigital(models.Model):
    name=models.CharField(u'名称',max_length=128,null=True)
    url = models.URLField(u'抓取地址',max_length=255, unique=True)  
    curl = models.URLField(u'评论地址',max_length=255,null=True) 
    price=models.CharField(u'价格',max_length=30,null=True)
    savedate = models.DateTimeField(u'保存时间',auto_now_add=True,blank=True,null=True)  
    img = models.ImageField(u'图片地址',upload_to = 'digital')
    
    processor=models.CharField(u'处理器型号',max_length=128,null=True)
    frequency=models.CharField(u'处理器主频',max_length=128,null=True)   
    storage=models.CharField(u'内存容量',max_length=128,null=True)    
    harddrive=models.CharField(u'硬盘容量',max_length=128,null=True)    
    screensize=models.CharField(u'屏幕尺寸',max_length=128,null=True)    
    Graphics=models.CharField(u'显卡芯片',max_length=128,null=True)
    markettime=models.CharField(u'上市日期',max_length=128,null=True)    
    system=models.CharField(u'操作系统',max_length=128,null=True)    
    weight=models.CharField(u'屏幕尺寸',max_length=128,null=True)       
    def __unicode__(self):  
        return "%s"%self.name

class NCamera(models.Model):
    name=models.CharField(u'名称',max_length=128,null=True)
    url = models.URLField(u'抓取地址',max_length=255, unique=True)  
    curl = models.URLField(u'评论地址',max_length=255,null=True) 
    price=models.CharField(u'价格',max_length=30,null=True)
    savedate = models.DateTimeField(u'保存时间',auto_now_add=True,blank=True,null=True)  
    img = models.ImageField(u'图片地址',upload_to = 'digital')
    
    pixel=models.CharField(u'有效像素数',max_length=128,null=True)   
    weight=models.CharField(u'产品重量',max_length=128,null=True)    
    screensize=models.CharField(u'显示屏尺寸',max_length=128,null=True)      
    markettime=models.CharField(u'发布日期',max_length=128,null=True)    
   
    def __unicode__(self):  
        return "%s"%self.name
        
class Review(models.Model):
    name=models.CharField(u'名称',max_length=128,null=True)
    url = models.URLField(u'评论地址',max_length=255)  
    pid = models.IntegerField(u'产品ID',null=True) 
    ptype=models.CharField(u'产品类型',max_length=30,null=True)
    savedate = models.DateTimeField(u'保存时间',auto_now_add=True,blank=True,null=True)  
        
    title=models.CharField(u'题目',max_length=128,null=True)   
    advantage=models.TextField(u'优点',null=True)    
    shortcoming=models.TextField(u'缺点',null=True)      
    summarize=models.TextField(u'总结',null=True)     
    score=models.FloatField(u'评分', null=True)
    credibility=models.FloatField(u'可信度', null=True)
    username=models.CharField(u'用户名',max_length=30,null=True)     
    sources=models.CharField(u'评论来源',max_length=50,null=True)     
    
   
    def __unicode__(self):  
        return "%s"%self.name
        
class Price(models.Model):
    name=models.CharField(u'名称',max_length=128,null=True)    
    pid = models.IntegerField(u'产品ID',null=True) 
    ptype=models.CharField(u'产品类型',max_length=30,null=True)
    savedate = models.DateTimeField(u'保存时间',auto_now_add=True,blank=True,null=True)  
    surl = models.URLField(u'商品地址',max_length=255)      
    sname=models.CharField(u'商品名称',max_length=128,null=True)
    spname=models.CharField(u'商家名称',max_length=128,null=True)
    price=models.FloatField(u'价格', null=True)
   
   
    def __unicode__(self):  
        return "%s"%self.name