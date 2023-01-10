from django.db import models
from django.conf import settings
from django.shortcuts import reverse

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE,default=None)
    slug = models.SlugField()
    discount_price = models.FloatField(default=0.1)


    def __str__(self):
        return "Art: "+str(self.name) + ",cena: "+str(self.price)+", kategoria: "+str(self.category)

    def get_absolute_url(self):
        return reverse("Product-View", kwargs={"slug": self.slug})

    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={"slug": self.slug})

    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={"slug": self.slug})

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def get_total_item_price(self):
        return round(self.quantity * self.product.price, 2)

    def get_total_discount_item_price(self):
        return round(self.quantity * self.product.discount_price,2)

    def get_amount_saved(self):
        return round(self.get_total_item_price() - self.get_total_discount_item_price(), 2)

    def get_final_price(self):
        if self.product.discount_price:
            return round(self.get_total_discount_item_price(), 2)
        return round(self.get_total_item_price(), 2)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    ordered = models.BooleanField(default=False)

    products = models.ManyToManyField(OrderItem)
    
    start_date = models.DateTimeField(auto_now_add=True)

    ordered_date = models.DateTimeField()
    
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)

    def get_total(self):
        total = 0
        for order_item in self.products.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total

    


