from django.urls import path

from .views import ReviewSearchView

urlpatterns = [
    path("/search", ReviewSearchView.as_view()),
]