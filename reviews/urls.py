from django.urls import path

from .views      import WholeReviewView

urlpatterns = [
    path("/whole", WholeReviewView.as_view()),
]