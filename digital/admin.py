# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 23:41:05 2011

@author: mark
"""

from django.contrib import admin
from shopping.digital.models import *

class Digital_Admin(admin.ModelAdmin):  
    list_display = ('name','price','savedate',)  
    ordering = ('-id',)  
    fields =('name','price','markettime') 

admin.site.register(NDigital, Digital_Admin) 