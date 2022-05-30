from django.urls import path

from .views      import ReviewDetailView

urlpatterns = [
    path("/<int:review_id>", ReviewDetailView.as_view())
]