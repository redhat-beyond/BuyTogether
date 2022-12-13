from django.contrib import admin
from delivery_location.models import DeliveryLocation


class DeliveryLocationAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'location',
                    'date', )


admin.site.register(DeliveryLocation, DeliveryLocationAdmin)
