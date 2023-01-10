from django.contrib import admin
from client.models import Client


class ClientAdmin(admin.ModelAdmin):
    list_display = ('client_account', 'area',)


admin.site.register(Client, ClientAdmin)
