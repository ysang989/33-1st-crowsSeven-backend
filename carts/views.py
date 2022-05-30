from django.views import View
import datetime

from django.http     import JsonResponse

from users.models    import User
from products.models import OptionProduct
from carts.models    import Cart
from utils           import login_decorator

class CartView(View):
    def delete(self, request, cart_id):
        try:
            product = Cart.objects.get(id = cart_id)
            product.delete()

            return JsonResponse({'results' : "DELETE_SUCCESS"}, status=200)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)