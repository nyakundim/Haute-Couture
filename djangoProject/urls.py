"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from . import views
from .views import (
    remove_from_cart,
    reduce_quantity_item,
    add_to_cart,
    Productdetail,
    # Casualdetail,
    # Streetweardetail,
    OrderSummaryView,
)
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="home"),  # INDEX PAGE
    path('athletic', views.product, name="athletic"),  # PRODUCT PAGE
    path('detail/<pk>', Productdetail.as_view(), name="detail"),  # DETAILED PRODUCT PAGE
    path('all-products', views.allproducts, name="all-products"),  # VIEW ALL PRODUCTS IN ONE PAGE
    # path('low-high', views.price_up, name="low-high"),  # VIEW ALL PRODUCTS IN ONE PAGE
    # path('high-low', views.price_down, name="high-low"),  # VIEW ALL PRODUCTS IN ONE PAGE
    path('streetwear', views.streetwear, name="streetwear"),  # VIEW STREETWEAR CATEGORY
    path('casual', views.casual, name="casual"),  # VIEW CASUAL CATEGORY
    path('filter', views.filter, name="filter"),  # VIEW CASUAL CATEGORY
    path('login', views.handlelogin, name="handlelogin"),
    path('logout', views.userlogout, name="logout"),
    path('feedback', views.feedback, name="feedback"),
    path('signup', views.handlesignup, name="handlesignup"),
    # path('casual/<pk>', Casualdetail.as_view(), name="casual"),
    # path('streetwear/<pk>', Streetweardetail.as_view(), name="streetwear"),
    path('order-summary', OrderSummaryView.as_view(), name='order-summary'),
    path('add-to-cart/<pk>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<pk>/', remove_from_cart, name='remove-from-cart'),
    path('reduce-quantity-item/<pk>/', reduce_quantity_item, name='reduce-quantity-item')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
