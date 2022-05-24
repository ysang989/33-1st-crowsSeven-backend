from django.db import models

class PhoneType(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table='phonetype'

class AirpotType(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table='airpottype'

class ShoeSize(models.Model):
    size = models.IntegerField()

    class Meta:
        db_table='shoesize'

class OptionProduct(models.Model):
    product    = models.ForeignKey('Product', on_delete=models.CASCADE)
    shoesize   = models.ForeignKey('ShoeSize', on_delete=models.CASCADE)
    phonetype  = models.ForeignKey('PhoneType', on_delete=models.CASCADE)
    airpottype = models.ForeignKey('AirpotType', on_delete=models.CASCADE)
    stock      = models.IntegerField(default=0)

    class Meta:
        db_table='optionproduct'

class Material(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        db_table='material'

class ProductCategory(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        db_table='productcategory'

class Product(models.Model):
    name                = models.CharField(max_length=50)
    width               = models.DecimalField(max_digits=10, decimal_places=5, null=True)
    weight              = models.DecimalField(max_digits=10, decimal_places=5, null=True)
    price               = models.DecimalField(max_digits=10, decimal_places=5)
    thumbnail_image_url = models.URLField(max_length=200)
    product_category    = models.ForeignKey('ProductCategory', on_delete=models.CASCADE)
    the_newest          = models.BooleanField(default=False)
    material            = models.ManyToManyField('Material')

    class Meta:
        db_table='product'




