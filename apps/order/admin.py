from django.contrib import admin

# Register your models here.
from apps.order.models import Order, OrderProducts


class OrderItemInLine(admin.TabularInline):
    model = OrderProducts
    extra = 1


@admin.register(OrderProducts)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "order",
        "quantity",
        "created_at",
    )


class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInLine,
    ]
    list_display = (
        "order_id",
        "created_at",
        "buyer",
        "ad_soyad",
        "payment_status",
        "status",
    )
    search_fields = (
        "order_id",
        'buyer__username',
        'buyer__first_name',
        'buyer__last_name',
    )
    list_filter = (
        "created_at",
        "payment_status",
        "status",
    )
    list_editable = ("status",)


    class Meta:
        model = Order


admin.site.register(Order, OrderAdmin)
