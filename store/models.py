import datetime

from django.db import models

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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_dirty = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True, db_index=True)


class Shipment(models.Model):
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
    image = models.ImageField()
    remark = models.TextField(null=True,blank=True)
    is_ready =models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

class QrProduct(models.Model):
    product_id = models.ForeignKey(PurchaseOrderProduct,on_delete=models.PROTECT,related_name='po_product')
    qr_code = models.ImageField()
    is_inbound_thai = models.BooleanField(default=False)
    is_outbound_china = models.BooleanField(default=False)
    is_outbound_thai = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

