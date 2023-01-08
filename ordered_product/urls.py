from django.urls import path
from ordered_product import views

urlpatterns = [
    path('orders', views.order_list, name="orders"),
    path('orders/<int:order_id>', views.change_quantity, name="orders"),
    path('orders/<int:order_id>,delete', views.delete_order, name="orders"),
    path('new_order', views.order, name="new_order"),
    path('new_order/', views.add_order, name="new_order"),
]
