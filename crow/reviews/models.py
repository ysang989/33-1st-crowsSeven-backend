from django.db    import models

from users.models import TimeStampedModel

class Review(TimeStampedModel):
    user          = models.ForeignKey('users.User', on_delete=models.CASCADE)
    optionproduct = models.ForeignKey('products.OptionProduct', on_delete=models.CASCADE)
    title         = models.CharField(max_length=30)
    context       = models.TextField(max_length=300)
    password      = models.CharField(max_length=100)
    view_count    = models.IntegerField()

    class Meta:
        db_table = "review"

class Comment(models.Model):
    user     = models.ForeignKey('users.User', on_delete=models.CASCADE)
    review   = models.ForeignKey('Review', on_delete=models.CASCADE)
    name     = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    content  = models.TextField(max_length=200)

    class Meta:
        db_table = "comment"       
