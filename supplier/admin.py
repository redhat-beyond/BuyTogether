from django.contrib import admin
from supplier.models import Supplier


class SupplierAdmin(admin.ModelAdmin):
    list_display = ('supplier_account', 'business_name',)


admin.site.register(Supplier, SupplierAdmin)
