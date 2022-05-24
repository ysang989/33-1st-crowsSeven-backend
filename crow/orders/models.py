from django.db    import models

from users.models import TimeStampedModel

class OrderStatus(models.Model):
    status = models.CharField(max_length=40)

    class Meta:
        db_table = "orderstatus"

class PaymentMethod(models.Model):
    payment = models.CharField(max_length=100)

    class Meta:
        db_table = "paymentmethod"

class DeliveryAddress(models.Model):
    deliveryaddress = models.CharField(max_length=200)

    class Meta:
        db_table = "deliveryaddress"

class Order(TimeStampedModel):
    user                     = models.ForeignKey('users.User', on_delete=models.CASCADE)
    present_delivery_address = models.ForeignKey('PresentDeliveryAddress', on_delete=models.CASCADE)
    order_status             = models.ForeignKey('OrderStatus', on_delete=models.CASCADE)
    count                    = models.IntegerField(default=0)
    shopping_fee             = models.IntegerField(default=3000)
    order_number             = models.CharField(max_length=50)

    class Meta:
        db_table = "order"

class PresentDeliveryAddress(models.Model):
    delivery_address    = models.CharField(max_length=300)
    delivery_email      = models.EmailField()
    recipient           = models.CharField(max_length=10)
    receive_phonenumber = models.IntegerField()
    delivery_message    = models.TextField(max_length=200, null=True)

    class Meta:
        db_table = 'presentdeliveryaddress'

class OrderItemStatus(models.Model):
    itemstatus = models.CharField(max_length=10)

    class Meta:
        db_table = 'orderitemstatus'

class OrderItem(models.Model):
    option_product    = models.ForeignKey('products.OptionProduct', on_delete=models.CASCADE)
    order             = models.ForeignKey('Order', on_delete=models.CASCADE)
    order_item_status = models.ForeignKey('OrderItemStatus', on_delete=models.CASCADE)
    shipping_company  = models.CharField(max_length=50)
    shipping_number   = models.CharField(max_length=100)
    count             = models.IntegerField(default=0)

    class Meta:
        db_table = "orderitem"

