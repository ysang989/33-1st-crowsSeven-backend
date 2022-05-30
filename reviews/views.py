from django.shortcuts import render

# Create your views here.
import json
import datetime

from django.views       import View
from django.http        import JsonResponse
from django.db.models   import Q
from django.shortcuts   import redirect

from reviews.models     import Review, Comment
from products.models    import Product
from orders.models      import Order, OrderItem
from products.models    import OptionProduct, Product
from users.models       import User
from utils              import login_decorator

class WholeReviewView(View):
    def get(self, request):
        try:
            reviews = Review.objects.order_by("-created_at")
            review_list =[{
                "review_id"        : review.id,
                "review_product"   : review.product.name,
                "review_title"     : review.title,
                "review_thumb_nail": review.product.thumbnail_image_url,
                "review_name"      : review.user.username,
                "review_date"      : review.updated_at,
                "review_view_count": review.view_count
            } for review in reviews]

            return JsonResponse({"message" : review_list}, status=200)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)