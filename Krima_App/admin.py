from django.contrib import admin
from .models import *

# Register your models here.

class Ord_pay_admin(admin.ModelAdmin):
    pass
admin.site.register(My_Upload_file,Ord_pay_admin)
