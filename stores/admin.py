from django.contrib import admin
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group

from stores import models

admin.site.unregister(Group)
admin.site.unregister(Site)

class ProductInline(admin.TabularInline):
    model = models.Product
    extra = 1

class OrderInline(admin.TabularInline):
    model = models.Order
    extra = 0

    inlines = [ProductInline]

    def queryset(self, request):
        qs = super(OrderInline, self).queryset(request)
        return qs.filter(ordered_on__isnull=False).order_by('ordered_on')


class StoreAdmin(admin.ModelAdmin):
    inlines = [ProductInline, OrderInline]
    list_filter = ('name', 'product__name')
    list_display = ('name',)


admin.site.register(models.Store, StoreAdmin)

'''

for store in models.Store.objects.all():
    class OrdersAdmin(admin.ModelAdmin):
        model = models.Order
        class Meta:
            verbose_name = '%s order' % store.name 

        def queryset(self, request):
            qs = super(OrdersAdmin, self).queryset(request)
            return qs.filter(ordered_on__isnull=False, store=store).order_by('ordered_on')

    admin.site.register(models.Order, OrdersAdmin)
'''

