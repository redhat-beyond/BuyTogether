from django.contrib import admin
from client.models import Client


class ClientAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'first_name', 'last_name',
                    'password', 'user_type', 'area',)


admin.site.register(Client, ClientAdmin)
