from django.db import models
from django.conf import settings
from django.shortcuts import reverse


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20)
    value = models.IntegerField()
    discount_price = models.IntegerField(blank=True, null=True)
    description = models.TextField()
    image = models.ImageField(upload_to='images')

    # Product.objects.get(category="")
    def get_absolute_url(self):
        return reverse("detail", kwargs={
            "pk": self.pk
        })

    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={
            "pk": self.pk
        })

    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={
            "pk": self.pk
        })

    class Meta:
        db_table = "Product"


class Feedback(models.Model):
    feedback = models.TextField()

    class Meta:
        db_table = "Feedback"


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.name}"

    def get_total_item_price(self):
        return self.quantity * self.item.value

    def get_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.name

    def get_total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total


# class Casual(models.Model):
#     name = models.CharField(max_length=100)
#     category = models.CharField(max_length=45)
#     value = models.IntegerField()
#     discount_price = models.FloatField(blank=True, null=True)
#     description = models.TextField()
#     image = models.ImageField(upload_to='images')
#
#     def get_absolute_url(self):
#         return reverse("casual", kwargs={
#             "pk": self.pk
#
#         })
#
#     def get_add_to_cart_url(self):
#         return reverse("add-to-cart", kwargs={
#             "pk": self.pk
#         })
#
#     def get_remove_from_cart_url(self):
#         return reverse("remove-from-cart", kwargs={
#             "pk": self.pk
#         })
#
#     class Meta:
#         db_table = "Casual"
#
#
# class Streetwear(models.Model):
#     name = models.CharField(max_length=100)
#     category=models.CharField(max_length=45)
#     value = models.IntegerField()
#     discount_price = models.FloatField(blank=True, null=True)
#     description = models.TextField()
#     image = models.ImageField(upload_to='images')
#
#     def get_absolute_url(self):
#         return reverse("streetwear", kwargs={
#             "pk": self.pk
#
#         })
#
#     def get_add_to_cart_url(self):
#         return reverse("add-to-cart", kwargs={
#             "pk": self.pk
#         })
#
#     def get_remove_from_cart_url(self):
#         return reverse("remove-from-cart", kwargs={
#             "pk": self.pk
#         })
#
#     class Meta:
#         db_table = "Streetwear"


