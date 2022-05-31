from django.urls import path

from .views import ProductDetailView,ProductListView


urlpatterns = [
    path('/<int:product_id>', ProductDetailView.as_view()),
    # GET :8000/products
    # GET :8000/products/1
    # POST :8000/products/1/review
    path('', ProductListView.as_view())
]
