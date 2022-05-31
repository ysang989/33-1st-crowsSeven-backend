from django.urls import path

from .views      import ReviewDetailView, ReviewView, WholeReviewView

urlpatterns = [
    path("/<int:review_id>", ReviewDetailView.as_view()),
    path("/product/<int:product_id>", ReviewView.as_view()),
    path("/whole", WholeReviewView.as_view()),

]