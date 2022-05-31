from django.urls import path

from .views      import ReviewView, WholeReviewView

urlpatterns = [
    path("/product/<int:product_id>", ReviewView.as_view()),
    path("/whole", WholeReviewView.as_view()),
]