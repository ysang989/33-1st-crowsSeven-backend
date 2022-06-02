from django.urls import path

from .views      import ReviewDetailView, ReviewView, WholeReviewView, ReviewSearchView

urlpatterns = [
    path("/<int:review_id>", ReviewDetailView.as_view()),
    path("/product/<int:product_id>", ReviewView.as_view()),
    path("/whole", WholeReviewView.as_view()),
    path("/search", ReviewSearchView.as_view()),
]
