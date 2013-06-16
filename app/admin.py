from django.contrib import admin
from app import models

admin.site.register(models.Store)
admin.site.register(models.Product)
admin.site.register(models.Order)


