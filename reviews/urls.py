from django.urls import path

from .views      import ReviewView

urlpatterns = [
    # :8000/reviews/product/1
    path("/product/<int:product_id>", ReviewView.as_view()),
]
