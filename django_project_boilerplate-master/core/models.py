from django.db import models
from django.conf import settings
from django.shortcuts import reverse

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE,default=None)
    slug = models.SlugField()


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


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    ordered = models.BooleanField(default=False)

    products = models.ManyToManyField(OrderItem)
    
    start_date = models.DateTimeField(auto_now_add=True)

    ordered_date = models.DateTimeField()

    


