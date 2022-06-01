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
            carts = Cart.objects.filter(created_at__lt = datetime.datetime.now() - datetime.timedelta(hours=24))
            if carts:
                [cart.delete() for cart in carts]
            
            cart_products = Cart.objects.select_related('option_product').filter(user_id = request.user.id)
            
            results = [{
                    "product_thumbnail_image_url": cart_product.option_product.product.thumbnail_image_url,
                    "product_name"               : cart_product.option_product.product.name,
                    "option_name"                : option_name,
                    "product_price"              : cart_product.option_product.product.price,
                    "product_count"              : cart_product.count,
                    "cart_id"                    : cart_product.id
                }for cart_product in cart_products]

            return JsonResponse({'results' : results}, status=200)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)