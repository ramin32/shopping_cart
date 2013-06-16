"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from app import models

class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client() 
        User.objects.create_user('test', 'temporary@gmail.com', 'test')
        models.Store.objects.create(name="test_store")

    def test_redirect_to_login(self):
        response = self.client.get('/test_store/', follow=True)
        self.assertEqual(response.redirect_chain[0][0], 'http://testserver/login/?next=/test_store/')
        self.assertEqual(response.redirect_chain[0][1], 302)

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
        
