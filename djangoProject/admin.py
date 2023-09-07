from django.contrib import admin

from .models import (Product, Feedback, OrderItem, Order)  # , Casual, Streetwear

admin.site.register(Product)
# admin.site.register(Casual)
# admin.site.register(Streetwear)
admin.site.register(Feedback)
admin.site.register(OrderItem)
admin.site.register(Order)
