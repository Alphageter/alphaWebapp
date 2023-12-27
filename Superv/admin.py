from django.contrib import admin
from .models import Salerep , Sales


class Salerepfields(admin.ModelAdmin):
    list_display=["numdepot","datedepot","timedepot"]

class Salesfields(admin.ModelAdmin):
    list_display=["numdepot","date","tt"]    
# Register your models here.

admin.site.register(Salerep,Salerepfields)
admin.site.register(Sales,Salesfields)