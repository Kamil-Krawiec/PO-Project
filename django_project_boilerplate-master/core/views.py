from django.shortcuts import render
from .models import Product
from django.views.generic import ListView,DetailView

class HomeView(ListView):
    model=Product
    template_name="home.html"


class ProductDetailView(DetailView):
    model=Product
    template_name="product.html"
