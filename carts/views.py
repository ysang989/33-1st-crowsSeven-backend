import datetime

from django.views    import View
from django.http     import JsonResponse

from products.models import OptionProduct
from carts.models    import Cart
from users.models    import User
from utils           import login_decorator

class CartView(View):
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
