"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from app import models

class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client() 
        self.user = User.objects.create_user('test', 'temporary@gmail.com', 'test')
        self.test_store = models.Store.objects.create(name="test_store")

    def test_redirect_to_login(self):
        response = self.client.get('/test_store/', follow=True)
        self.assertRedirects(response, 'http://testserver/login/?next=/test_store/')

        self.client.login(username='test', password='test')
        response = self.client.get('/test_store/', follow=True)
        self.assertFalse(response.redirect_chain)
        self.assertEqual(response.status_code, 200)

    def test_store_page(self):
        self.client.login(username='test', password='test')
        response = self.client.get('/test_store/')
        self.assertEqual(response.status_code, 200)

        self.client.login(username='test', password='test')
        response = self.client.get('/test_store_1/')
        self.assertEqual(response.status_code, 404)

    def test_add_to_cart(self):
        cart, created = models.Cart.objects.get_or_create(store=self.test_store, user=self.user)
        self.assertEqual(len(cart.products.all()), 0)

        # make request
        self.client.login(username='test', password='test')
        product = models.Product.objects.create(name="test product",
                                                description="test description",
                                                price=20.00,
                                                image="test.jpg",
                                                quantity=20,
                                                store=self.test_store)
        response = self.client.post(reverse('add_to_cart', kwargs=dict(store_name=self.test_store.name, product_id=product.id)))

        # verify state
        cart = models.Cart.objects.get(store=self.test_store, user=self.user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(cart.products.all()), 1)
        self.assertEqual(cart.products.all()[0], product)
        self.assertJSONEqual(response.content, '{"new_total": "20"}')





        
