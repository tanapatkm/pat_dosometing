import datetime
from django.db.models.signals import pre_save
from django.utils.crypto import get_random_string
from django.conf import settings as appsettings
import qrcode
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from users.models import User


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120,default='')
    tel = models.CharField(max_length=220,default='')
    is_in_thai = models.BooleanField(default=True)
    is_in_china = models.BooleanField(default=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return '{} [{}]'.format(self.id, self.name)


class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    client_id = models.CharField(max_length=255,default='')
    name = models.CharField(max_length=120,default='')
    line_id = models.CharField(max_length=120,default='')
    tel = models.CharField(max_length=220,default='')
    email = models.EmailField(max_length=200,default='')
    address = models.CharField(max_length=220,default='')
    zipcode = models.CharField(max_length=220,default='')
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return '{} [{}]'.format(self.id, self.client_id)

class BuyerCBM(models.Model):
    type = models.CharField(max_length=120)
    cbm_rate = models.DecimalField(max_digits=5,decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    remark = models.TextField()
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, null=True)

class Drop(models.Model):
    name = models.CharField(max_length=120, unique=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=120, unique=True)
    sortno = models.PositiveIntegerField()
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICE = (
        ('pending', 'Pending'),
        ('decline', 'Decline'),
        ('approved', 'Approved'),
        ('processing', 'Processing'),
        ('complete', 'Complete'),
        ('bulk', 'Bulk'),
    )
    supplier = models.ForeignKey(Employee, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    design = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, null=True)
    drop = models.ForeignKey(Drop, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE)
    created_date = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.product.name


class Delivery(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    courier_name = models.CharField(max_length=120)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.courier_name

class Warehouse(models.Model):
    name = models.CharField(max_length=255, db_index=True, null=False)
    location = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.name



class Packinglist(models.Model):
    packing_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255,null=False,default='')
    status = models.BooleanField(max_length=255, default=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_dirty = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True, db_index=True)

    def __str__(self):
        return self.name

class Shipment(models.Model):
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
    STATUS = [
        (ACTIVE, 'active'),
        (INACTIVE, 'inactive'),

    ]
    name = models.CharField(max_length=255,null=False,default='')
    status = models.CharField(max_length=255, choices=STATUS, null=False, default=ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_dirty = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True, db_index=True)
    packing_id = models.ForeignKey(Packinglist, on_delete=models.PROTECT, related_name='packing_list',null=True)

    def __str__(self):
        return self.name
class PurchaseOrder(models.Model):
    OWNER = 'OWNER'
    SERVICE = 'SHIPPING PROVIDER'
    SHIPPING_CHOICES = [
        (OWNER, 'Owner Shipping'),
        (SERVICE, 'SHIPPING PROVIDER'),
    ]

    INTRANSIT_CHINA = 'INTRANSIT_CHINA'
    INTRANSIT_THAI = 'INTRANSIT_THAI'
    OUTBOUND_THAI ='OUTBOUND_THAI'
    STATUS = [
        (INTRANSIT_CHINA,'intransit_china'),
        (INTRANSIT_THAI,'intransit_thai'),
        (OUTBOUND_THAI, 'outbound_thai'),

    ]
    po_id = models.BigAutoField(primary_key=True)
    po_number = models.CharField(max_length=255,db_index=True,null=False)
    type = models.CharField(max_length=255, db_index=True, null=False)
    status = models.CharField(max_length=255, choices=STATUS, null=False, default=INTRANSIT_CHINA)
    is_paid = models.BooleanField(default=False)
    shipping_by = models.CharField(max_length=25, choices=SHIPPING_CHOICES, null=False, default=OWNER)
    is_dirty = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True, db_index=True)
    price = models.IntegerField(default=0,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    track_no = models.CharField(max_length=255,null=True)
    sack_id = models.ForeignKey(Shipment, on_delete=models.PROTECT, related_name='containers',null=True)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, null=True,related_name='buyer')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, null=True,related_name='warehouse')

    def __str__(self):
        return self.po_number



class PurchaseOrderProduct(models.Model):
    type = models.CharField(max_length=255, db_index=True, null=False)
    brand = models.CharField(max_length=255, db_index=True, null=False)
    packing_type = models.CharField(max_length=255, db_index=True, null=False)
    canton = models.IntegerField(default=1)
    weight = models.CharField(max_length=255, db_index=True, null=False)
    wight = models.CharField(max_length=255, db_index=True, null=False)
    lenght = models.CharField(max_length=255, db_index=True, null=False)
    height = models.CharField(max_length=255, db_index=True, null=False)
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to='images')
    remark = models.TextField(null=True,blank=True)
    is_ready =models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    po_id = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, null=True,related_name='po')

class QrProduct(models.Model):
    product_id = models.ForeignKey(PurchaseOrderProduct,on_delete=models.PROTECT,related_name='po_product')
    product_name = models.CharField(max_length=255,default='')
    qr_code = models.ImageField(upload_to='qr_code',blank=True)
    is_inbound_thai = models.BooleanField(default=False)
    is_outbound_china = models.BooleanField(default=False)
    is_outbound_thai = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

# @receiver(post_save, sender=QrProduct)
# def create_qrcode(sender, instance, created, **kwargs):
#     if not instance.string:  # We need to check if we want to create
#         qr = qrcode.QRCode(
#             version=1,
#             error_correction=qrcode.constants.ERROR_CORRECT_L,
#             box_size=10,
#             border=4, )
#         qr.add_data(instance.string)
#         img = qr.make_image()
#         codepwd = appsettings.MEDIA_ROOT + "qr/" + instance.string + ".png"
#         img.save(codepwd)
#         instance.qr_code = "qr/" + instance.string + ".png"
