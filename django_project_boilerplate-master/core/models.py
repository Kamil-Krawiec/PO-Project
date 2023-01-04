from django.db import models
from django.conf import settings

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()

    def __str__(self):
        return str(self.name) + str(self.price)


class OrderItem(models.Model):
    
    product = models.ForeignKey(Product,on_delete=models.CASCADE)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    ordered = models.BooleanField(default=False)

    products = models.ManyToManyField(OrderItem)
    
    start_date = models.DateTimeField(auto_now_add=True)

    ordered_date = models.DateTimeField()

    


