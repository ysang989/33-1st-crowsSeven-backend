from django.urls import path

from .views      import ReviewView

urlpatterns = [
    path("/<int:review_id>", ReviewView.as_view()),
]
