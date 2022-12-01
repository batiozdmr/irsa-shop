from django.contrib import admin

# Register your models here.
from .models import CouponCodeList,CouponCodeCreate



class CuponListAdmin(admin.ModelAdmin):
    list_display = ('coupon_create', 'code', 'price')



class CuponCreateAdmin(admin.ModelAdmin):
    list_display = ('name', 'count', 'price')




admin.site.register(CouponCodeList,CuponListAdmin)
admin.site.register(CouponCodeCreate,CuponCreateAdmin)
