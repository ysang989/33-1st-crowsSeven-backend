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

            count               = data["count"]
            selected_product_id = data["option_product_id"]

            cart_products = Cart.objects.select_related('option_product').filter(user_id = request.user)
            carts         = cart_products.filter(option_product = selected_product_id)

            if carts.exists():
                cart        = carts.get(option_product_id = OptionProduct.objects.get(id=selected_product_id))
                cart.count += int(count)
                cart.save()

            else:
                Cart.objects.create(
                    user           = request.user,
                    option_product = OptionProduct.objects.get(id=selected_product_id),
                    count          = count
                )

            return JsonResponse({'message' : "success"}, status=201)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)