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
    def patch(self, request, cart_id):
        try:
            data = json.loads(request.body)

            count   = data["qty"]
            product = Cart.objects.filter(id = cart_id)
            product.update(count = count)

            return JsonResponse({'results' : "success"}, status=200)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
    