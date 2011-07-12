from django.contrib import admin
from shopping.phone.models import *

class Phone_Admin(admin.ModelAdmin):  
    list_display = ('name','price','savedate',)  
    ordering = ('-id',)  
    fields =('name','price','markettime') 

admin.site.register(Phone, Phone_Admin) 
admin.site.register(NPhone, Phone_Admin) 
