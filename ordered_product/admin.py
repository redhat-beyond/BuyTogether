from django.contrib import admin
from ordered_product.models import OrderedProduct


class OrderedProductAdmin(admin.ModelAdmin):
    list_display = ('delivery_location_id', 'user_name', 'supplier_product_id', 'quantity', )


admin.site.register(OrderedProduct, OrderedProductAdmin)
