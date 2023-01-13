from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.core.exceptions import ValidationError
from django.db.models import Avg
import uuid
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

PAYMENT_CHOICES = (
    ('B', 'Blik'),
    ('P', 'Przelew'),
    ('G','Gotowka')
)

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'


def validate_rate(value):
    if value>5 or value<0:
        raise ValidationError(
            ('%(value)s is not proper'),
            params={'value': value},
        )    

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

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    products = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(Address, related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(Address, related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.CharField(max_length=1,choices=PAYMENT_CHOICES)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)


    def get_total(self):
        total = 0
        for order_item in self.products.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total

    def get_items_sum(self):
        total = 0
        for order_item in self.products.all():
            total += 1
        return total

    
class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.review


