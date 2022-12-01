from django.contrib import admin

# Register your models here.


from django.contrib.auth.admin import UserAdmin

from apps.accounts.models import  Address,CityList,EmailPool
from django.contrib.auth.models import Group, User

class AddressInLine(admin.TabularInline):
    model = Address
    extra = 1



admin.site.register(CityList)
admin.site.register(Address)
admin.site.register(EmailPool)
