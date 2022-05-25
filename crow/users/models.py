from django.db import models

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class User(TimeStampedModel):
    name                    = models.CharField(max_length=10)
    ID                      = models.CharField(max_length=30, unique=True)
    password                = models.CharField(max_length=120)
    address                 = models.CharField(max_length=120)
    phone_number            = models.IntegerField()
    birth_date              = models.DateField()
    optional_agreement      = models.JSONField()
    email                   = models.CharField(max_length=30)

    class Meta:
        db_table='users'

class MainImage(models.Model):
    main_image_url = models.URLField(max_length=200)

    class Meta:
        db_table = "main_images"