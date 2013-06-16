import json

from django.contrib import auth 
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse

from users import forms

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
            return render(request, 'users/register.html', {'form': form})

    return render(request, 'users/register.html', {'form': forms.RegisterForm()})

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
        return render(request, 'users/login.html', {'form': form})

    return render(request, 'users/login.html', {'form': forms.LoginForm()})

@login_required
def logout(request):
    auth.logout(request)
    return redirect('login')
