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
    def post(self, request):
        try:
            data       = json.loads(request.body)
            user       = User.objects.get(id=request.user)
            title      = data["title"]
            context    = data["context"]
            password   = data["password"]
            product    = data["product"]
            product_id = Product.objects.get(name=product)

            if Review.objects.filter(Q(product_id=product)&Q(user_id=user.id)).exists():
                return JsonResponse({'message':'REVIEW_ALREADY_EXIST'}, status=404)

            Review.objects.create(
                user       = user,
                title      = title,
                context    = context,
                password   = password,
                view_count = 0,
                product    = product_id
            )

            return JsonResponse({"message" : "SUCCESS"}, status=201)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)