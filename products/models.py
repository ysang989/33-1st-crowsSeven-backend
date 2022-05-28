from django.db import models

class PhoneType(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table='phonetypes'

class AirpotType(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table='airpottypes'

class ShoeSize(models.Model):
    size = models.IntegerField()

    class Meta:
        db_table='shoesizes'

class OptionProduct(models.Model):
    product     = models.ForeignKey('Product', on_delete=models.CASCADE)
    shoe_size   = models.ForeignKey('ShoeSize', on_delete=models.CASCADE, null=True)
    phone_type  = models.ForeignKey('PhoneType', on_delete=models.CASCADE, null=True)
    airpot_type = models.ForeignKey('AirpotType', on_delete=models.CASCADE, null=True)
    stock       = models.IntegerField(default=0)

    class Meta:
        db_table='option_products'

class Material(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        db_table='materials'

class ProductCategory(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        db_table='product_categories'

class Product(models.Model):
    name                = models.CharField(max_length=50)
    description         = models.TextField(max_length=300)
    width               = models.DecimalField(max_digits=6,decimal_places=3, null=True)
    weight              = models.DecimalField(max_digits=6,decimal_places=3, null=True)
    price               = models.DecimalField(max_digits=8,decimal_places=2)
    thumbnail_image_url = models.URLField(max_length=200)
    product_category    = models.ForeignKey('ProductCategory', on_delete=models.CASCADE)
    the_newest          = models.BooleanField(default=False)
    material            = models.ManyToManyField('Material')
    optional_existence   = models.BooleanField(default=0)

    class Meta:
        db_table='products'

class DetailImage(models.Model):
    product          = models.ForeignKey('Product', on_delete=models.CASCADE)
    detail_image_url = models.URLField(max_length=200)

    class Meta:
        db_table='detail_images'


