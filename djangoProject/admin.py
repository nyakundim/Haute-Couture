from django.contrib import admin
from .models import (Product, Feedback, OrderItem, Order)  # , Casual, Streetwear

# admin.site.register(Casual)
# admin.site.register(Streetwear)
admin.site.register(OrderItem)
admin.site.register(Order)


class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "value")


admin.site.register(Product, ProductAdmin)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("id", "feedback")


admin.site.register(Feedback, FeedbackAdmin)
