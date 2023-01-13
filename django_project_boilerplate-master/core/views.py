from django.shortcuts import render, get_object_or_404,redirect
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.views.generic import ListView,DetailView,View
from django.utils import timezone
from .forms import ReviewForm


class HomeView(ListView):
    model=Product
    template_name="home.html"




class ProductDetailView(DetailView):
    model=Product
    template_name="product.html"

def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.products.filter(product__slug=product.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("order-summary")
        else:
            order.products.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.products.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("order-summary")





class OrderSummaryView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.products.filter(product__slug=product.slug).exists():
            order_item = OrderItem.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            order.products.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("Product-View", slug=slug)

    else:
        messages.info(request, "You do not have an active order")
        return redirect("Product-View", slug=slug)



def remove_single_item_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.products.filter(product__slug=product.slug).exists():
            order_item = OrderItem.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.products.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("Product-View", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("Product-View", slug=slug)


def submit_review(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        # try:
        #     reviews = ReviewRating.objects.get(product=id)
        #     form = ReviewForm(request.POST, instance=reviews)
        #     form.save()
        #     messages.success(request, 'Thank you! Your review has been updated.')
        #     return redirect(url)
        # except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                product = get_object_or_404(Product, id=id)
                data.product = product
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)

def all_reviews(request,id):
    product = get_object_or_404(Product, id=id)
    review_list = ReviewRating.objects.filter(product = product)
    context = {
        "product": product,
        "review_list": review_list
    }
    return render(request, "product.html", context)