import datetime
import json

from django.views    import View
from django.http     import JsonResponse

from products.models import OptionProduct
from carts.models    import Cart
from users.models    import User
from utils           import login_decorator

class CartView(View):
    @login_decorator
    def post(self, request):
        try:
            data       = json.loads(request.body)
            user        = request.user
            count               = data["count"]
            selected_product_id = data["option_product_id"]
            
            cart_products = Cart.objects.select_related('option_product').filter(user_id = request.user)
            cart, created  = Cart.objects.get_or_create(

                    user            = user,
                    option_product  = selected_product_id,
                    defaults        = {'count' : count },
                )

            if not created:
                cart.count += int(count)
                cart.save()
               
            return JsonResponse({'message' : "success"}, status=201)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)