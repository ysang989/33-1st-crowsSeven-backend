from django.urls import path

from .views import ProductDetailView


urlpatterns = [
    path('/product/<int:id>', ProductDetailView.as_view())
]