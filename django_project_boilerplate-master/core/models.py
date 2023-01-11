from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.core.exceptions import ValidationError

# Create your models here.

def validate_rate(value):
    if value>5 or value<0:
        raise ValidationError(
            ('%(value)s is not proper'),
            params={'value': value},
        )    

class Rating(models.Model):
    rate = models.FloatField(validators=[validate_rate])
    ratings = models.IntegerField(default=0)

    def __str__(self) -> str:
        return str(self.rate)


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
    stars = models.ForeignKey(Rating,on_delete=models.CASCADE,default=None,blank=True )

    def __str__(self):
        return "Art: "+str(self.name) + ",cena: "+str(self.price)+", kategoria: "+str(self.category)

    def get_absolute_url(self):
        return reverse("Product-View", kwargs={"slug": self.slug})

    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={"slug": self.slug})

    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={"slug": self.slug})

    def set_new_rate(self,rate):
        self.stars.rate = ((self.stars.ratings*self.stars.rate)+rate)/(self.stars.ratings+1)


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def get_total_item_price(self):
        return self.quantity * self.product.price

    def get_total_discount_item_price(self):
        return self.quantity * self.product.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.product.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


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

    
