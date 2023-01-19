from django.urls import path
from ordered_product import views

urlpatterns = [
     path('orders/<int:order_id>', views.change_quantity, name="orders"),
     path('orders/<int:order_id>,delete', views.delete_order, name="orders"),
     path('new_order/', views.order, name="new_order"),
     path('new_order/search_product_by_product_name',
          views.get_products_by_product_name, name="search_product_by_product_name"),
     path('new_order/search_product_by_location',
          views.get_products_by_client_area, name="search_product_by_location"),
     path('new_order/search_supplier_catalog_by_user_name',
          views.get_products_by_supplier_user_name, name="search_supplier_catalog_by_business_name"),
     path('new_order/find_delivery/<int:supplier_product_id>',
          views.find_delivery, name="find_delivery"),
     path('new_order/order_summary/<int:supplier_product_id>,<int:delivery_location_id>',
          views.order_summary, name="order_summary"),
     path('new_order/complete_order/<int:supplier_product_id>,<int:delivery_location_id>',
          views.complete_order, name="complete_order"),
     path('new_order/pay_order', views.pay_order, name="search_supplier_catalog_by_business_name"),
]
