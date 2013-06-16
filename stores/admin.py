from django.contrib import admin

from stores import models

admin.site.register(models.Store)
admin.site.register(models.Product)
admin.site.register(models.Order)


