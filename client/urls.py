from django.urls import path
from client import views


urlpatterns = [
    path('', views.clients_page, name="client page"),
]
