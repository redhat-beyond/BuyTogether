from django.urls import path
from supplier import views


urlpatterns = [
    path('', views.suppliers_page, name="suppliers page"),
]
