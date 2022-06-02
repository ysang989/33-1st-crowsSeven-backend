from django.urls import path, include

urlpatterns = [
    path("users", include("users.urls")),
    path('products', include('products.urls')),
    path('orders', include('orders.urls')),
    path('reviews', include('reviews.urls')),
    path('reviews', include('reviews.urls')),
    path('carts', include('carts.urls')),
]
