from django.shortcuts import render
from .models import Product


def product_list(request):
    context = {
        'items': Product.objects.all()
    }

    return render(request,"product_list.html",context)