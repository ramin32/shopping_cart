"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

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

    def test_redirect_to_login(self):
        response = self.client.get('/stores/test_store/', follow=True)
        self.assertRedirects(response, 'http://testserver/users/login/?next=/stores/test_store/')

        self.client.login(username='test', password='test')
        response = self.client.get('/stores/test_store/', follow=True)
        self.assertFalse(response.redirect_chain)
        self.assertEqual(response.status_code, 200)
