import json

from django.views       import View
from django.http        import JsonResponse

from orders.models      import Order
from products.models    import OptionProduct
from utils              import login_decorator

class ReviewView(View):
    @login_decorator
    def get(self, request):
        try:
            total_option_product     = []
            selected_products_names  = []
            selected_products        = []
            total_option             = []

            total_order=Order.objects.filter(user_id=request.user).select_related('user').\
                prefetch_related('orderitem_set')

            for total_option_product in total_order:
                total_option.append(list(total_option_product.orderitem_set.values('option_product_id')))

            total_option_product_names = sum(total_option,[])
            
            [selected_products.append(total_option_product_names[i]['option_product_id'])\
                for i in range(len(total_option_product_names))]

            selected_products_names = [{
                "product_name"  : OptionProduct.objects.get(id=selected_product).product.name,
                "product_id" : OptionProduct.objects.get(id=selected_product).product.id
            } for selected_product in selected_products ]
           
            selected_products_names = list({selected_products_name['product_name']:selected_products_name for selected_products_name in selected_products_names}.values())
            return JsonResponse({"message" : selected_products_names}, status=200)
            
        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
