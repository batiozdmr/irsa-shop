from django.contrib import admin
from django.contrib import admin

# Register your models here.


# Register your models here.
from apps.product.models import *
from mptt.admin import DraggableMPTTAdmin


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('text', 'alt')
    # list_filter = ('text', 'season', 'alignment', 'created_at',)


class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'title')
    list_filter = ('product',)


class ProductequestListAdmin(admin.ModelAdmin):
    list_display = ('product', 'user')
    list_filter = ('product',)


class ProductFavoriteListAdmin(admin.ModelAdmin):
    list_display = ('product', 'user')
    list_filter = ('product',)


class ProductAdmin(admin.ModelAdmin):
    filter_horizontal = ('images',)
    exclude = ('product_type',)

    list_display = ('name', 'category', 'price', 'stock', 'best_product', 'best_selling_product', 'latest_product')
    list_filter = ('best_product', 'best_selling_product', 'latest_product')
    list_editable = ['price', 'stock', 'best_product', 'best_selling_product', 'latest_product']


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)

admin.site.register(ProductComment, ProductCommentAdmin)
admin.site.register(ProductRequestList, ProductequestListAdmin)
admin.site.register(ProductFavoriteList, ProductequestListAdmin)
admin.site.register(Category, DraggableMPTTAdmin)
admin.site.register(ProductType)


class AttributesAdmin(admin.ModelAdmin):
    list_display = ('text', 'default_value', 'getPro', 'total')


admin.site.register(Attributes, AttributesAdmin)
admin.site.register(ShippingMethod)

admin.site.register(OrderStatus)
admin.site.register(CargoCompany)
