from django.contrib import admin
from supplier.models import Supplier


class SupplierAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'first_name', 'last_name',
                    'password', 'business_name',)


admin.site.register(Supplier, SupplierAdmin)
