from django.urls import path

from .views      import CommentView

urlpatterns = [
    path("/<int:review_id>/comment", CommentView.as_view()),
]