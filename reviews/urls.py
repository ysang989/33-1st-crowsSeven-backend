from django.urls import path

from .views      import ReviewView, WholeReviewView

urlpatterns = [
    path("/<int:review_id>", ReviewView.as_view()),
    path("/whole", WholeReviewView.as_view()),
]
