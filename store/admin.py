from django.contrib import admin

from .models import (
    Employee,
    Buyer,
    Drop,
    Product,
    Order,
    Delivery,
PurchaseOrder
)

class SupplierAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'tel', 'created_date']

class BuyerAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'address', 'created_date']

admin.site.register(Employee, SupplierAdmin)
admin.site.register(Buyer, BuyerAdmin)
admin.site.register(Drop)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Delivery)
admin.site.register(PurchaseOrder)