import json
import datetime

from django.views       import View
from django.http        import JsonResponse
from django.db.models   import Q
from django.shortcuts   import redirect

from reviews.models     import Review, Comment
from products.models    import Product
from orders.models      import Order, OrderItem
from products.models    import OptionProduct, Product
from users.models       import User
from utils              import login_decorator

class ReviewView(View):
    @login_decorator
    def get(self, request):
        try:
            total_option_product    = []
            selected_products_name  = []
            total_option_product_id = []
            total_option            = []
            selected_products       = []

            total_order=Order.objects.filter(user_id=request.user).select_related('user').prefetch_related('orderitem_set')

            for total_option_product in total_order:
                total_option.append(list(total_option_product.orderitem_set.values('option_product_id')))

            total_option_product_names = sum(total_option,[])

            for total_option_product_name in total_option_product_names:
                total_option_product_id.append(list(map(dict,set(tuple(sorted(total_option_product_names.items()))))))

            [selected_products.append(total_option_product_id[i]['option_product_id']) for i in range(len(a))]

            [selected_products_name.append(OptionProduct.objects.get(id=j).product.name) for selected_product in selected_products]
            
            return JsonResponse({"message" : list(set(c))}, status=200)
            
        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
