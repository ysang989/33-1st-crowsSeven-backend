from django.db import models

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class User(TimeStampedModel):
    name                    = models.CharField(max_length=10)
    username                = models.CharField(max_length=30, unique=True)
    password                = models.CharField(max_length=120)
    address                 = models.CharField(max_length=120)
    phone_number            = models.CharField(max_length=50)
    birth_date              = models.CharField(max_length=20, null=True)
    optional_agreement      = models.BooleanField(default=0)
    email                   = models.CharField(max_length=30)

    class Meta:
        db_table='users'