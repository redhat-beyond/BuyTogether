from django.contrib import admin
from buy_together_app.models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('qr_code', 'product_name', 'description', )


admin.site.register(Product, ProductAdmin)
