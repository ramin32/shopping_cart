from django import forms

from stores import models


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = ['credit_card_type', 'credit_card_number', 'security_number', 'expiration_month', 'expiration_year', 'address', 'city', 'state', 'zip_code', 'phone_number']
