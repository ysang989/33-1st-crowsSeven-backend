from django.views import View
import datetime

from django.http     import JsonResponse

from products.models import OptionProduct
from carts.models    import Cart
from users.models  import User
from utils         import login_decorator

class CartView(View):
    @login_decorator
    def get(self, request):
        try:
            product_id          = request.GET.get('product_id', None)
            option_name         = request.GET.get('option_name', None)
            count               = request.GET.get('count', None)
            selected_product_id = request.GET.get('option_product_id', None)

            if product_id:
                selected_product = OptionProduct.objects.get(id=selected_product_id)

                if Cart.objects.filter(option_product = selected_product_id).exists():
                    cart = Cart.objects.get(option_product = selected_product_id)
                    cart.count += int(count)
                    cart.save()

                else:
                    Cart.objects.update_or_create(
                        user           = User.objects.get(id=request.user),
                        option_product = OptionProduct.objects.get(id=selected_product.id),
                        count          = count
                    )

                carts = Cart.objects.filter(user_id = request.user)

                for cart in carts:
                    if cart.created_at == datetime.datetime.now() -datetime.timedelta(minutes=10):
                        cart.delete()

                results = [{
                    "product_thumbnail_image_url": cart.option_product.product.thumbnail_image_url,
                    "product_name"               : cart.option_product.product.name,
                    "option_name"                : option_name,
                    "product_price"              : cart.option_product.product.price,
                    "product_count"              : cart.count
                }for cart in carts]

            else:
                carts = Cart.objects.filter(user_id = request.user)
                for cart in carts:
                    if cart.created_at == datetime.datetime.now() -datetime.timedelta(minutes=10):
                        cart.delete()

                results = [{
                    "product_thumbnail_image_url": cart.option_product.product.thumbnail_image_url,
                    "product_name"               : cart.option_product.product.name,
                    "option_name"                : option_name,
                    "product_price"              : cart.option_product.product.price,
                    "product_count"              : cart.count,
                    "cart_id"                    : cart.id
                }for cart in carts]

            return JsonResponse({'results' : results}, status=200)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
            
        except OptionProduct.DoesNotExist :
            return JsonResponse({"message" : "INVALID_PROUDCT_OPTION"}, status=400)
