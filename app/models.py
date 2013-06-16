from django.db import models
from django.contrib.auth.models import User

class Store(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='product_images')
    store = models.ForeignKey(Store)

    def __unicode__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User)
    products = models.ForeignKey(Store)
    submitted = models.BooleanField(default=False)

    def __unicode__(self):
        return self.user.username
