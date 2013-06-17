from datetime import datetime

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from stores import models

class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client() 
        self.user = User.objects.create_user('test', 'temporary@gmail.com', 'test')
        self.test_store = models.Store.objects.create(name="test_store")

    def test_store_page(self):
        self.client.login(username='test', password='test')
        response = self.client.get('/stores/test_store/')
        self.assertEqual(response.status_code, 200)

        self.client.login(username='test', password='test')
        response = self.client.get('/stores/test_store_1/')
        self.assertEqual(response.status_code, 404)

    def test_add_to_cart(self):
        cart = models.Order.get_cart(store=self.test_store, user=self.user)
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
        cart = models.Order.objects.get(store=self.test_store, user=self.user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(cart.products.all()), 1)
        self.assertEqual(cart.products.all()[0], product)
        self.assertJSONEqual(response.content, '{"new_total": "20"}')
        return cart

    
    def test_checkout(self):
        cart = self.test_add_to_cart()
        now = datetime.now()
        response = self.client.post(reverse('checkout_cart', kwargs=dict(store_name=self.test_store.name)),
                                    dict(name_on_card='test_name', 
                                              credit_card_type = 'Visa',
                                              credit_card_number = '1234123412341234',
                                              security_number = '123',
                                              expiration_month = '12',
                                              expiration_year = str(now.year + 5),
                                              address = '123 broadway',
                                              city = 'brooklyn',
                                              state = 'NY',
                                              zip_code = '11210',
                                              phone_number = '7188881234'))
        response = self.client.post(reverse('confirm_order', kwargs=dict(store_name=self.test_store.name, order_id=cart.id)), follow=True)
        order = models.Order.objects.get(id=cart.id)
        self.assertTrue(order.ordered_on != None)
        self.assertContains(response, 'Thank you for your order!')

    def test_delete_order(self):
        cart = self.test_add_to_cart()

        now = datetime.now()
        response = self.client.post(reverse('checkout_cart', kwargs=dict(store_name=self.test_store.name)),
                                    dict(name_on_card='test_name', 
                                              credit_card_type = 'Visa',
                                              credit_card_number = '1234123412341234',
                                              security_number = '123',
                                              expiration_month = '12',
                                              expiration_year = str(now.year + 5),
                                              address = '123 broadway',
                                              city = 'brooklyn',
                                              state = 'NY',
                                              zip_code = '11210',
                                              phone_number = '7188881234'))
        response = self.client.post(reverse('delete_order', kwargs=dict(store_name=self.test_store.name, order_id=cart.id)), follow=True)

        self.assertContains(response, 'Your order has been deleted')







        
