import json
import datetime

from django.views    import View
from django.http     import JsonResponse

from users.models    import User
from carts.models    import Cart
from products.models import OptionProduct
from utils           import login_decorator

class CartView(View):
    @login_decorator
    def delete(self, request, cart_id):
        try:
            cart = Cart.objects.get(id = cart_id)
            cart.delete()

            return JsonResponse({'message' : "DELETE_SUCCESS"}, status=201)

        except Cart.DoesNotExist:
            return JsonResponse({"message" : "CART_NOT_EXISTED"}, status=400)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

    @login_decorator
    def patch(self, request, cart_id):
        try:
            data = json.loads(request.body)

            count   = data["qty"]
            cart    = Cart.objects.get(id=cart_id)

            if cart.option_product.stock < count:
                return JsonResponse({"message" : "STUFF_OVERFLOW"}, status=400) 
                
            else:
                cart.count = count
                cart.save()
                
            return JsonResponse({'message' : "SUCCESS"}, status=201)

        except Cart.DoesNotExist:
            return JsonResponse({'message' : "CART_NOT_EXISTED"}, status=201)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
    
    @login_decorator
    def get(self, request):
        try:
            Cart.objects.filter(created_at__lt = datetime.datetime.now() - datetime.timedelta(hours=24)).delete()
            
            cart_products = Cart.objects.select_related('option_product').filter(user_id = request.user.id)
            
            data = [{
                    'id'     : cart_product.id,
                    'product': cart_product.option_product.product.thumbnail_image_url,
                    'info'   : cart_product.option_product.product.name,
                    'price'  : cart_product.option_product.product.price,
                    'qty'    : cart_product.count,
                    
                } for cart_product in cart_products]

            return JsonResponse({'results' : data}, status=200)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
