from django.shortcuts import render, get_object_or_404,redirect
from .models import *
from django.views.generic import ListView,DetailView
from django.utils import timezone

class HomeView(ListView):
    model=Product
    template_name="home.html"


class ProductDetailView(DetailView):
    model=Product
    template_name="product.html"


def add_to_cart(request,slug):
    product = get_object_or_404(Product,slug=slug)
    order_item,created = OrderItem.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False
        )

    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.products.filter( product__slug = product.slug).exists():
            order_item.quantity+=1
            order_item.save()
        else:
            order.products.add(order_item)


    else:
        order = Order.objects.create(user=request.user,ordered_date = timezone.now())
        order.products.add(order_item)

    return redirect("Product-View",slug=slug)

