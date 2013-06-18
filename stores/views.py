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
    store = get_object_or_404(models.Store, name=request.subdomain)
    cart = models.Order.get_cart(store=store, user=request.user)
    return render(request, 'stores/index.html', {'store': store, 'cart': cart})

@login_required
@csrf_exempt
def cart(request, product_id=None, checkout_form=None):
    store = get_object_or_404(models.Store, name=request.subdomain)
    cart = models.Order.get_cart(store=store, user=request.user)
    if request.method == 'POST' and product_id:
        product = get_object_or_404(models.Product, id=product_id)
        cart.add_product(product)
        return HttpResponse(json.dumps({'new_total': str(cart.total())}), content_type="application/json")
    return render(request, 'stores/cart.html', {'store': store, 'cart': cart, 'checkout_form': checkout_form or forms.CheckoutForm()})

@login_required
@csrf_exempt
def remove_from_cart(request, product_id):
    store = get_object_or_404(models.Store, name=request.subdomain)
    cart = models.Order.get_cart(store=store, user=request.user)
    product = get_object_or_404(models.Product, id=product_id)
    cart.remove_product(product)
    return redirect('cart')


@login_required
def checkout_cart(request):
    if request.method == 'POST':
        store = get_object_or_404(models.Store, name=request.subdomain)
        order = models.Order.get_cart(store=store, user=request.user)
        form = forms.CheckoutForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return render(request, 'stores/confirm_order.html', {'store': store, 'order': order, 'checkout_form': forms.CheckoutForm()})
        else:
            return cart(request, checkout_form=form)
    raise Http404

@login_required
def confirm_order(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(models.Order, id=order_id, user=request.user)
        order.ordered_on = datetime.now()
        order.save()
        for pq in order.productquantities_set.all():
            if pq.quantity > pq.product.quantity:
                messages.error(request, 
                               '%s %ss were available for purchase, please try again when items are back in stock.' % (pq.product.quantity, pq.product.name))
                pq.quantity = pq.product.quantity
                pq.product.quantity = 0
            else:
                pq.product.quantity -= pq.quantity
            pq.product.save()
        messages.success(request, 'Thank you for your order!')
        return redirect('index')
    raise Http404

@login_required
def delete_order(request, order_id):
    order = get_object_or_404(models.Order, id=order_id, user=request.user)
    order.delete()
    messages.success(request, 'Your order has been deleted')
    return redirect('index')

@login_required
def past_orders(request):
    store = get_object_or_404(models.Store, name=request.subdomain)
    cart = models.Order.get_cart(store=store, user=request.user)
    orders = models.Order.objects.filter(user=request.user, store=store, ordered_on__isnull=False)
    return render(request, 'stores/past_orders.html', {'store': store, 'cart': cart, 'orders': orders, 'checkout_form': forms.CheckoutForm()})






