from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from core.views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('',HomeView.as_view(),name="Home-View"),
    path('product/<slug>/',ProductDetailView.as_view(),name="Product-View"),
    path('add-to-cart/<slug>/',add_to_cart,name="add-to-cart"),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path('cart/',OrderSummaryView.as_view(),name="order-summary"),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    path('submit_review/<id>/', submit_review, name='submit_review'),
    path('all_reviews/<id>', all_reviews, name='all_reviews'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('checkout/success', success_view, name='success'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
