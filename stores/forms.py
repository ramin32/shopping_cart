from django.contrib.auth.models import User
from django import forms

from stores import models



class BillingInformationForm(forms.ModelForm):
    class Meta:
        model = models.BillingInformation

                                            
