from django.contrib import admin
from product.models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('qr_code', 'product_name', 'description', )


admin.site.register(Product, ProductAdmin)
