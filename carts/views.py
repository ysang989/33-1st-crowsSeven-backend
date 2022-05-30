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

            count               = request.GET.get('count', None)
            selected_product_id = request.GET.get('option_product_id', None)
            option_name         = request.GET.get('option_name', None)

            cart_products = Cart.objects.select_related('option_product').filter(user_id = request.user)
            carts = cart_products.filter(option_product = selected_product_id)

            if selected_product_id:
                if carts.exists():
                    cart = carts.get(option_product_id = OptionProduct.objects.get(id=selected_product_id))
                    cart.count += int(count)
                    cart.save()

                else:
                    Cart.objects.create(
                        user           = User.objects.get(id=request.user),
                        option_product = OptionProduct.objects.get(id=selected_product_id),
                        count          = count
                    )
    
            results = [{
                "product_thumbnail_image_url": cart.option_product.product.thumbnail_image_url,
                "product_name"               : cart.option_product.product.name,
                "option_name"                : option_name,
                "product_price"              : cart.option_product.product.price,
                "product_count"              : cart.count,
                "cart_id"                    : cart.id
            } for cart in cart_products]

            return JsonResponse({'results' : results}, status=200)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
            
        except OptionProduct.DoesNotExist :
            return JsonResponse({"message" : "INVALID_PROUDCT_OPTION"}, status=400)
