import json

from django.contrib import auth 
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.forms.util import ErrorList
from django.views.decorators.csrf import csrf_exempt

from stores import forms, models


@login_required
def index(request):
    stores = models.Store.objects.all()
    return render(request, 'stores/index.html', {'stores': stores})

@login_required
def store(request, store_name):
    store = get_object_or_404(models.Store, name=store_name)
    cart = models.Order.get_cart(store=store, user=request.user)
    return render(request, 'stores/store.html', {'store': store, 'cart': cart})

@login_required
@csrf_exempt
def cart(request, store_name, product_id=None):
    store = get_object_or_404(models.Store, name=store_name)
    cart = models.Order.get_cart(store=store, user=request.user)
    if request.method == 'POST' and product_id:
        product = get_object_or_404(models.Product, id=product_id)
        cart.add_product(product)
        return HttpResponse(json.dumps({'new_total': str(cart.total())}), content_type="application/json")


    return render(request, 'stores/cart.html', {'store': store, 'cart': cart})

@login_required
@csrf_exempt
def remove_from_cart(request, store_name, product_id):
    store = get_object_or_404(models.Store, name=store_name)
    cart, created = models.Order.objects.get_or_create(store=store, user=request.user)
    product = get_object_or_404(models.Product, id=product_id)
    cart.remove_product(product)
    return redirect('cart', store_name=store_name)


@login_required
def checkout_cart(request, store_name):
    store = get_object_or_404(models.Store, name=store_name)
    cart, created = models.Cart.objects.get_or_create(store=store, user=request.user)
    form = forms.BillingInformationForm()
    return HttpResponse('checkout')

