from django.urls import path

from .views      import ReviewView

urlpatterns = [
    path("/write", ReviewView.as_view()),
]