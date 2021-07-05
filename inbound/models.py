from django.db import models

from users.models import User


class Warehouse(models.Model):
    name = models.CharField(max_length=255, db_index=True, null=False)
    location = models.TextField(null=True,blank=True)

class Container(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_dirty = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True, db_index=True)
    max_quantity = models.IntegerField(default=90)
    current_quantity = models.PositiveIntegerField

class Packinglist(models.Model):
    packing_id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_dirty = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True, db_index=True)
    con_id = models.ForeignKey(Container, on_delete=models.PROTECT, related_name='packing_list')


class Sack(models.Model):
    type = models.CharField(max_length=255, db_index=True, null=False)
    status = models.CharField(max_length=255, db_index=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_dirty = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True, db_index=True)
    packing_id = models.ForeignKey(Packinglist, on_delete=models.PROTECT, related_name='packing_list')

class PurchaseOrder(models.Model):
    OWNER = 'OWNER'
    SERVICE = 'SHIPPING PROVIDER'
    SHIPPING_CHOICES = [
        (OWNER, 'Owner Shipping'),
        (SERVICE, 'SHIPPING PROVIDER'),
    ]
    INTRANSIT = 'INTRANSIT'
    CANCELLED = 'CANCELLED'
    DELIVERIED ='DELIVERIED'
    INBOUND ='INBOUNED'
    PENDING ='PENDING'
    STATUS = [
        (INTRANSIT,'in_transit'),
        (CANCELLED,'cancelled'),
        (DELIVERIED, 'cancelled'),
        (INBOUND, 'inbound'),
        (PENDING, 'pending'),

    ]
    po_id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=255, db_index=True, null=False)
    status = models.CharField(max_length=255, choices=STATUS, null=False, default=INBOUND)
    is_paid = models.BooleanField(default=False)
    shipping_by = models.CharField(max_length=25, choices=SHIPPING_CHOICES, null=False, default=OWNER)
    is_dirty = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    sack_id = models.ForeignKey(Sack, on_delete=models.PROTECT, related_name='containers')


class PurchaseOrderProduct(models.Model):
    type = models.CharField(max_length=255, db_index=True, null=False)
    brand = models.CharField(max_length=255, db_index=True, null=False)
    packing_type = models.CharField(max_length=255, db_index=True, null=False)
    canton = models.IntegerField()
    weight = models.CharField(max_length=255, db_index=True, null=False)
    wight = models.CharField(max_length=255, db_index=True, null=False)
    lenght = models.CharField(max_length=255, db_index=True, null=False)
    height = models.CharField(max_length=255, db_index=True, null=False)
    remark = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)