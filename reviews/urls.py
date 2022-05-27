from django.urls import path

from .views import ReviewView, CommentView

urlpatterns = [
    path("/review/<int:option_product_id>", ReviewView.as_view()),
    path("/review/<int:option_product_id>/comment", CommentView.as_view()),
]
