import json
import datetime

from django.views       import View
from django.http        import JsonResponse
from django.db.models   import Q

from reviews.models     import Review, Comment
from products.models    import Product
from orders.models      import Order, OrderItem
from products.models    import OptionProduct, Product
from users.models       import User
from utils              import login_decorator
from django.shortcuts   import redirect

class ReviewView(View):
    @login_decorator
    def delete(self, request, review_id):
        try:
            review = Review.objects.get(id=review_id)
            review.delete()

            return redirect('/')
            
        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)