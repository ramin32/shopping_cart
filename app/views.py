import json

from django.contrib import auth 
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.forms.util import ErrorList
from django.views.decorators.csrf import csrf_exempt

from app import forms, models

def register(request):
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data['username'],
                                            form.cleaned_data['email'],
                                            form.cleaned_data['password'])
            user.save()
            user = auth.authenticate(username=form.cleaned_data['username'], 
                                     password=form.cleaned_data['password'])

            auth.login(request, user)
            return redirect('index')
        else:
            return render(request, 'app/register.html', {'form': form})

    return render(request, 'app/register.html', {'form': forms.RegisterForm()})

def login(request):
    login_errors = None
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data['username'], 
                                     password=form.cleaned_data['password'])
            if user and user.is_active:
                auth.login(request, user)
                return redirect('index')

        errors = form._errors.setdefault("__all__", ErrorList())
        errors.append(u"Account not found")
        return render(request, 'app/login.html', {'form': form})

    return render(request, 'app/login.html', {'form': forms.LoginForm()})

@login_required
def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required
def index(request):
    stores = models.Store.objects.all()
    return render(request, 'app/index.html', {'stores': stores})

@login_required
def store(request, store_name):
    store = get_object_or_404(models.Store, name=store_name)
    cart, created = models.Cart.objects.get_or_create(store=store, user=request.user)
    return render(request, 'app/store.html', {'store': store, 'cart': cart})

@login_required
@csrf_exempt
def cart(request, store_name, product_id=None):
    store = get_object_or_404(models.Store, name=store_name)
    cart, created = models.Cart.objects.get_or_create(store=store, user=request.user)
    if request.method == 'POST' and product_id:
        product = get_object_or_404(models.Product, id=product_id)
        cart.products.add(product)
        cart.save()
        return HttpResponse(json.dumps({'new_total': str(cart.total())}), content_type="application/json")


    return render(request, 'app/cart.html', {'store': store, 'cart': cart})




@login_required
def checkout_cart(request, store_name):
    store = get_object_or_404(models.Store, name=store_name)
    cart, created = models.Cart.objects.get_or_create(store=store, user=request.user)
    form = forms.BillingInformationForm()
    return HttpResponse('checkout')

