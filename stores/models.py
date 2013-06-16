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
    quantity = models.IntegerField()
    store = models.ForeignKey(Store)

    def __unicode__(self):
        return self.name


class BillingInformation(models.Model):
    credit_card_type = models.CharField(max_length=50)
    credit_card_number = models.CharField(max_length=20)
    security_number = models.CharField(max_length=4)
    expiration_month = models.IntegerField()
    expiration_year = models.IntegerField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10)

    def __unicode__(self):
        return "%s %s" % (self.credit_card_type, self.credit_card_number[-4:])

class Cart(models.Model):
    user = models.ForeignKey(User)
    store = models.ForeignKey(Store)
    products = models.ManyToManyField(Product)

    def total(self):
        return sum([p.price for p in self.products.all()]) 


class Order(models.Model):
    user = models.ForeignKey(User)
    products = models.ManyToManyField(Product)
    store = models.ForeignKey(Store)
    billing_information = models.ForeignKey(BillingInformation)
    submitted_on = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=8, decimal_places=2) # in case prices change
   
    def __unicode__(self):
        return self.user.username

