from django.urls import path
from . import views


app_name = 'supplier_product'
urlpatterns = [
    path('increase_quantity/<int:id>/<int:n>/', views.increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:id>/<int:n>/', views.decrease_quantity, name='decrease_quantity'),
]
