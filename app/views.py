from django.contrib import auth 
from django.http import Http404
from django.shortcuts import render

import forms

def login(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data['username'], 
                                     password=form.cleaned_data['password'])
            if user and user.is_active:
                auth.login(request, user)
    return render(request, 'app/login.html', {'form':forms.LoginForm()})
