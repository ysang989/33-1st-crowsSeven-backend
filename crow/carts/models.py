from django.db import models

from users.models import TimeStampedModel

class Cart(TimeStampedModel):
    user           = models.ForeignKey('users.User', on_delete=models.CASCADE)
    count          = models.IntegerField()
    option_product = models.ForeignKey('products.OptionProduct', on_delete=models.CASCADE)

    class Meta:
        db_table = "carts"    
