from django.contrib import admin

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group

from app import models

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.unregister(Site)

admin.site.register(models.Store)
admin.site.register(models.Product)
admin.site.register(models.Order)


