import json
import uuid

from django.views       import View
from django.http        import JsonResponse
from django.db.models   import Q
from django.db          import transaction


from utils              import login_decorator
from products.models    import OptionProduct
from carts.models       import Cart
from users.models       import User
from orders.models      import (
    OrderItemStatus,
    OrderItem, Order,
    OrderStatus,
    PaymentMethod,
    PresentDeliveryAddress
)

class OrderView(View):
    @login_decorator
    def post(self, request):
        try:
            data                = json.loads(request.body)
            user                = request.user
            shopping_fee        = data["shopping_fee"]
            paymentmethod       = data["paymentmethod"]
            delivery_address    = data["delivery_address"]
            delivery_email      = data["delivery_email"]
            recipient           = data["recipient"]
            receive_phonenumber = data["receive_phonenumber"]
            delivery_message    = data["delivery_message"]
            selected_cart_ids   = data["selected_product_ids"]

            with transaction.atomic():
                address = PresentDeliveryAddress.objects.create(
                    delivery_address         = delivery_address,
                    delivery_email           = delivery_email,
                    recipient                = recipient,
                    receive_phonenumber      = receive_phonenumber,
                    delivery_message         = delivery_message,
                )

                order = Order.objects.create(
                    user                     = user,
                    order_number             = uuid.uuid4(),
                    order_status             = OrderStatus.objects.get(status ="주문완료"),
                    present_delivery_address = address,
                    shopping_fee             = shopping_fee,
                    paymentmethod            = PaymentMethod.objects.get(id = paymentmethod)
                )

                for selected_cart_id in selected_cart_ids:
                    cart_item = Cart.objects.get(id = selected_cart_id)
                    OrderItem.objects.create(
                        order             = order,
                        option_product    = cart_item.option_product,
                        shipping_company  = "cj",
                        shipping_number   = uuid.uuid4(),
                        count             = cart_item.count,
                        order_item_status = OrderItemStatus.objects.get(item_status = "주문완료"),
                    )
                    cart_item.delete()

                    results=[]
                    results=[{
                        "order_count" : order.order_number,
                        "order_item"  : order.created_at 
                    }]

            return JsonResponse({'message' : results}, status=200)

        except Cart.DoesNotExist:
            return JsonResponse({"message" : "CART_NOT_EXISTED"}, status=400)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)