from django.contrib.auth.models import User

from django import forms


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

class RegisterForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField()

    def clean_username(self):
        username = self.cleaned_data.get('username')
        users = User.objects.filter(username=username).all()
        if users:
            raise forms.ValidationError("Username exists")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        users = User.objects.filter(email=email).all()
        if users:
            raise forms.ValidationError("Email exists")
        return email



    def clean_confirm_password(self):
        if self.cleaned_data.get('password') != self.cleaned_data.get('confirm_password'):
            raise forms.ValidationError("Passwords don't match!")
        return self.cleaned_data.get('confirm_password')
                                            
