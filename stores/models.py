from datetime import date

from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


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

class ProductQuantities(models.Model):
    product = models.ForeignKey('Product')
    order = models.ForeignKey('Order')
    quantity = models.IntegerField()

class Order(models.Model):
    user = models.ForeignKey(User)
    products = models.ManyToManyField(Product, through=ProductQuantities)
    store = models.ForeignKey(Store)

    credit_card_type = models.CharField(max_length=50, 
                                        choices=[(t,t) for t in ('Visa', 'MasterCard', 'American Express', 'Discover')],
                                        null=True)
    credit_card_number = models.CharField(max_length=20, null=True)
    security_number = models.CharField(max_length=4, null=True)
    expiration_month = models.IntegerField(choices=[(m, m) for m in xrange(1,13)], null=True)

    _current_year = date.today().year
    expiration_year = models.IntegerField(choices=[(y, y) for y in xrange(_current_year, _current_year + 20)], null=True)
    address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=255, null=True)
    zip_code = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=10, null=True)

    ordered_on = models.DateTimeField(null=True)
    shipped_on = models.DateTimeField(null=True)


    def total(self):
        return sum([pq.product.price * pq.quantity for pq in self.productquantities_set.all()]) 

    def add_product(self, product):
        product_quantity = None
        try:
            product_quantity = ProductQuantities.objects.get(order=self, product=product)
            product_quantity.quantity += 1
            product_quantity.save()
        except ProductQuantities.DoesNotExist:
            product_quantity = ProductQuantities.objects.create(order=self, product=product, quantity=1)

    def remove_product(self, product):
        try:
            product_quantity = ProductQuantities.objects.get(order=self, product=product)
            product_quantity.quantity -= 1
            if product_quantity.quantity > 0:
                product_quantity.save()
            else:
                product_quantity.delete()
        except ProductQuantities.DoesNotExist:
            pass








    @classmethod
    def get_cart(cls, store, user):
        cart, created = cls.objects.get_or_create(store=store, user=user, ordered_on__isnull=True)
        return cart

   
    def __unicode__(self):
        return self.user.username

