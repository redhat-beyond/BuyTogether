"""buy_together URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from buy_together_app import views


urlpatterns = [
    path('', views.main_page, name="Main Page"),
    path('description', views.description_page, name="Website Description"),
    path('login', views.log_in_page, name="Log In"),
    path('logout', views.logout_user, name="Log Out"),
    path('not_allowed', views.not_allowed_page, name="Not allowed"),
    path('signup', views.signup_user, name="Sign Up"),
    path('signup/supplier', views.signup_supplier, name="Sign Up Supplier"),
    path('signup/client', views.signup_client, name="Sign Up Client"),
]
