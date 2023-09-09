from django.contrib import admin
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
import json

from .models import (Product, Feedback, OrderItem, Order)  # , Casual, Streetwear

# admin.site.register(Casual)
# admin.site.register(Streetwear)
admin.site.register(OrderItem)
admin.site.register(Order)


class ProductAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ("id", "name", "category", "value")
    search_fields = ("name", "category")
    search_help_text = "search name or category"
    list_filter = ("category",)


admin.site.register(Product, ProductAdmin)


# def changelist_view(self, request, extra_context=None):
#     # Retrieve the count of books per original publication year
#     value = (
#         Product.objects
#         .values("category")
#         .annotate(y=Count("id"))
#         .order_by("-category")
#     )
#
#     # Convert the queryset to JSON format
#     value_as_json = json.dumps(list(value), cls=DjangoJSONEncoder)
#
#     # Pass the JSON data to the changelist view's extra_context
#     extra_context = extra_context or {"value": value_as_json}
#
#     # Call the superclass changelist_view method with the updated extra_context
#     return super().changelist_view(request, extra_context=extra_context)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("id", "feedback")


admin.site.register(Feedback, FeedbackAdmin)
