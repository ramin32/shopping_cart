import json
from datetime import datetime

from django.contrib import auth 
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.forms.util import ErrorList
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

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
def cart(request, store_name, product_id=None, checkout_form=None):
    store = get_object_or_404(models.Store, name=store_name)
    cart = models.Order.get_cart(store=store, user=request.user)
    if request.method == 'POST' and product_id:
        product = get_object_or_404(models.Product, id=product_id)
        cart.add_product(product)
        return HttpResponse(json.dumps({'new_total': str(cart.total())}), content_type="application/json")
    return render(request, 'stores/cart.html', {'store': store, 'cart': cart, 'checkout_form': checkout_form or forms.CheckoutForm()})

@login_required
@csrf_exempt
def remove_from_cart(request, store_name, product_id):
    store = get_object_or_404(models.Store, name=store_name)
    cart = models.Order.objects.get_or_create(store=store, user=request.user)
    product = get_object_or_404(models.Product, id=product_id)
    cart.remove_product(product)
    return redirect('cart', store_name=store_name)


@login_required
def checkout_cart(request, store_name):
    if request.method == 'POST':
        store = get_object_or_404(models.Store, name=store_name)
        order = models.Order.get_cart(store=store, user=request.user)
        form = forms.CheckoutForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return render(request, 'stores/confirm_order.html', {'store': store, 'order': order, 'checkout_form': forms.CheckoutForm()})
        else:
            return cart(request, store_name, checkout_form=form)
    raise Http404

@login_required
def confirm_order(request, store_name, order_id):
    if request.method == 'POST':
        order = get_object_or_404(models.Order, id=order_id, user=request.user)
        order.ordered_on = datetime.now()
        order.save()
        for pq in order.productquantities_set.all():
            pq.product.quantity -= pq.quantity
            pq.product.save()
        messages.success(request, 'Thank you for your order!')
        return redirect('store', store_name=store_name)
    raise Http404

@login_required
def delete_order(request, store_name, order_id):
    order = get_object_or_404(models.Order, id=order_id, user=request.user)
    order.delete()
    messages.success(request, 'Your order has been deleted')
    return redirect('store', store_name=store_name)






