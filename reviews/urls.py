from django.urls import path

from .views      import WholeReviewView

urlpatterns = [
    path("/", WholeReviewView.as_view()),
]