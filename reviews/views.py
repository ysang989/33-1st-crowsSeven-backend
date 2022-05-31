import json
import datetime

from django.views       import View
from django.http        import JsonResponse
from django.db.models   import Q

from reviews.models     import Review
from products.models    import Product
from users.models       import User
from utils              import login_decorator

class ReviewView(View):
    @login_decorator
    def post(self, request, product_id):
        try:
            data       = json.loads(request.body)
            title      = data["title"]
            context    = data["context"]
            password   = data["password"]

            if Review.objects.filter(product_id=product_id , user_id = request.user).exists():
                return JsonResponse({'message':'REVIEW_ALREADY_EXIST'}, status=404)
            
            Review.objects.create(
                user       = request.user,
                title      = title,
                context    = context,
                password   = password,
                view_count = 0,
                product    = Product.objects.get(id=product_id),
            )

            return JsonResponse({"message" : "SUCCESS"}, status=201)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)