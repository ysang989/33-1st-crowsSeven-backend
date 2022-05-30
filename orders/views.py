import json
import uuid

from django.views       import View
from django.http        import JsonResponse
from django.db.models   import Q

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
            user                 = request.user
            shopping_fee         = data["shopping_fee"]
            paymentmethod        = data["paymentmethod"]
            delivery_address     = data["delivery_address"]
            delivery_email       = data["delivery_email"]
            recipient            = data["recipient"]
            receive_phonenumber  = data["receive_phonenumber"]
            delivery_message     = data["delivery_message"]
            selected_product_ids = data["option_product_id"][1]

            address = PresentDeliveryAddress.objects.create(
                delivery_address         = delivery_address,
                delivery_email           = delivery_email,
                recipient                = recipient,
                receive_phonenumber      = receive_phonenumber,
                delivery_message         = delivery_message,
            )

            order = Order.objects.create(
                user                     = User.objects.get(id=user),
                order_number             = uuid.uuid4(),
                order_status             = OrderStatus.objects.get(status ="주문완료"),
                present_delivery_address = address,
                shopping_fee             = shopping_fee,
                paymentmethod            = PaymentMethod.objects.get(payment = paymentmethod)
            )


            if selected_product_id:
                for selected_product_id in selected_product_ids:
                    order_item = OrderItem.objects.create(
                        order = order,
                        option_product = cart.option_product,
                        shipping_company = "cj",
                        shipping_number  = uuid.uuid4(),
                        count = cart.count,
                        order_item_status = OrderItemStatus.objects.get(item_status = "입금전"),
                        )

            else:
                carts   = Cart.objects.filter(user_id=user)

                for cart in carts :
                    order_item = OrderItem.objects.create(
                        order = order,
                        option_product = cart.option_product,
                        shipping_company = "cj",
                        shipping_number  = uuid.uuid4(),
                        count = cart.count,
                        order_item_status = OrderItemStatus.objects.get(item_status = "입금전"),
                        )

            carts.delete()
                
            results=[{
                "order_count": order.order_number,
                "order_time" : order.created_at
            }]

            return JsonResponse({'results' : results}, status=200)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)