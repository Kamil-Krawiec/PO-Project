from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from core.views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve 

urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')) ,
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    # path('',HomeView.as_view(),name="Home-View"),
    path('',home_view,name="home_view"),
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
    path('history/', order_history, name='success'), 
    path('history/order/<id>', order_details, name='details'),
    path('request-refund/<id>',refound_get, name='request-refund'),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
]
handler404 = "core.views.page_not_found_view"

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)



