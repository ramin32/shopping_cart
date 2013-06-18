from django.contrib import admin
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group

from stores import models

admin.site.unregister(Group)
admin.site.unregister(Site)

class ProductInline(admin.TabularInline):
    model = models.Product
    extra = 1

class ProductQuantitiesInline(admin.TabularInline):
    model = models.ProductQuantities
    extra = 1


class StoreAdmin(admin.ModelAdmin):
    inlines = [ProductInline]
    list_filter = ['name']
    list_display = ['name']
    search_fields = ['name', 'product__name']


admin.site.register(models.Store, StoreAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_filter = ['store__name']
    search_fields = ['name', 'description', 'store']
    list_display = ['store', 'name', 'price_string', 'quantity']

admin.site.register(models.Product, ProductAdmin)

class OrdersAdmin(admin.ModelAdmin):
    model = models.Order
    inlines = [ProductQuantitiesInline]
    list_filter = ['store__name']
    search_fields = ['user__first_name', 'user__last_name', 'user__username', 'product__name'] 
    list_display = ['store', 'user', 'ordered_on', 'total']

    def queryset(self, request):
        qs = super(OrdersAdmin, self).queryset(request)
        return qs.filter(ordered_on__isnull=False).order_by('ordered_on')

admin.site.register(models.Order, OrdersAdmin)

