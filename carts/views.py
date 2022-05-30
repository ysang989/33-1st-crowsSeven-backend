import datetime

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
            option_product_count = request.GET.get('qty')
            product              = Cart.objects.get(id = cart_id)
            
            product.count = option_product_count
            product.save()

            return JsonResponse({'results' : "success"}, status=200)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
    