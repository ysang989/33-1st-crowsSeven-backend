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
            total_option_product    = []
            selected_products_name  = []
            selected_products       = []
            total_option            = []

            total_order=Order.objects.filter(user_id=request.user).select_related('user').prefetch_related('orderitem_set')

            for total_option_product in total_order:
                total_option.append(list(total_option_product.orderitem_set.values('option_product_id')))

            total_option_product_names = sum(total_option,[])
            
            [selected_products.append(total_option_product_names[i]['option_product_id']) for i in range(len(total_option_product_names))]

            selected_products_name = [{
                "제품이름"  : OptionProduct.objects.get(id=selected_product).product.name,
                "제품아이디" : OptionProduct.objects.get(id=selected_product).product.id
            } for selected_product in selected_products ]
           
            selected_products_name = list({v['제품이름']:v for v in selected_products_name}.values())
            return JsonResponse({"message" : selected_products_name}, status=200)
            
        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
