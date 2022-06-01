import json

from django.views    import View
from django.http     import JsonResponse

from carts.models    import Cart
from utils           import login_decorator

class CartView(View):
    @login_decorator
    def patch(self, request, cart_id):
        try:
            data = json.loads(request.body)

            count   = data["qty"]
            product = Cart.objects.get(id=cart_id)

            if product.option_product.stock < count:
                return JsonResponse({"message" : "STUFF_OVERFLOW"}, status=400) 
                
            else:
                product.count = count
                product.save()
                
            return JsonResponse({'message' : "SUCCESS"}, status=201)

        except Cart.DoesNotExist:
            return JsonResponse({'message' : "CART_NOT_EXISTED"}, status=201)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
    