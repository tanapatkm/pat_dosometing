from django import forms
from django.forms import modelformset_factory

from .models import *


class EmployeeForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'name',
        'data-val': 'true',
        'data-val-required': 'Please enter name',
    }))
    is_in_thai = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'class': 'form-control',
        'id': 'address',
        'data-val': 'true',
        'data-val-required': 'Please enter tel',
    }))
    tel = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'tel',
        'data-val': 'true',
        'data-val-required': 'Please enter telephone',
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'id': 'email',
        'data-val': 'true',
        'data-val-required': 'Please enter email',
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'username',
        'data-val': 'true',
        'data-val-required': 'Please enter username',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'password',
        'data-val': 'true',
        'data-val-required': 'Please enter password',
    }))
    retype_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'retype_password',
        'data-val': 'true',
        'data-val-required': 'Please enter retype_password',
    }))


class BuyerForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'name',
        'data-val': 'true',
        'data-val-required': 'Please enter name',
    }))
    client_id = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'client_id',
        'data-val': 'true',
        'data-val-required': 'Please enter client_id',
    }))
    line_id = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'line_id',
        'data-val': 'true',
    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'client_id',
        'data-val': 'true',
        'data-val-required': 'Please enter address',
    }))
    tel = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'client_id',
        'data-val': 'true',
    }))
    zipcode = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'client_id',
        'data-val': 'true',
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'id': 'email',
        'data-val': 'true',
        'data-val-required': 'Please enter email',
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'username',
        'data-val': 'true',
        'data-val-required': 'Please enter username',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'password',
        'data-val': 'true',
        'data-val-required': 'Please enter password',
    }))
    retype_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'retype_password',
        'data-val': 'true',
        'data-val-required': 'Please enter retype_password',
    }))


class DropForm(forms.ModelForm):
    class Meta:
        model = Drop
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'name'})
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'sortno']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'name'}),
            'sortno': forms.NumberInput(attrs={'class': 'form-control', 'id': 'sortno'})
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['supplier', 'product', 'design', 'color', 'buyer', 'drop']

        widgets = {
            'supplier': forms.Select(attrs={'class': 'form-control', 'id': 'supplier'}),
            'product': forms.Select(attrs={'class': 'form-control', 'id': 'product'}),
            'design': forms.TextInput(attrs={'class': 'form-control', 'id': 'design'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'id': 'color'}),
            'buyer': forms.Select(attrs={'class': 'form-control', 'id': 'buyer'}),
            'drop': forms.Select(attrs={'class': 'form-control', 'id': 'drop'}),
        }


class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = '__all__'

        widgets = {
            'order': forms.Select(attrs={'class': 'form-control', 'id': 'order'}),
            'courier_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'courier_name'}),
        }


class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'name'}),
            'locations': forms.TextInput(attrs={'class': 'form-control', 'id': 'locations'}),
        }


class PackinglistForm(forms.ModelForm):
    class Meta:
        model = Packinglist
        fields = ['status']

        widgets = {
            'status': forms.CheckboxInput(attrs={'class': 'form-control', 'id': 'status'}),
        }


ShipmentFormset = modelformset_factory(
    Shipment,
    fields=('id',),
    extra=1,
    widgets={
        'id': forms.Select(
            attrs={
                'class': 'form-control',
                'placeholder': 'Select Shipment'
            }
        )
    }
)


class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = ['status', 'packing_id']

        widgets = {
            'status': forms.CheckboxInput(attrs={'class': 'form-control', 'id': 'status'}),
            'packing_id': forms.Select(attrs={'class': 'form-control', 'id': 'packing_id'}),
        }


class PoForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['po_number', 'type', 'is_paid', 'shipping_by', 'track_no', 'price', 'buyer', 'warehouse']

        widgets = {
            'po_number': forms.TextInput(attrs={'class': 'form-control', 'id': 'po_number'}),
            'type': forms.TextInput(attrs={'class': 'form-control', 'id': 'type'}),
            'is_paid': forms.CheckboxInput(attrs={'class': 'form-control', 'id': 'is_paid'}),
            'shipping_by': forms.Select(attrs={'class': 'form-control', 'id': 'shipping_by'}),
            'track_no': forms.TextInput(attrs={'class': 'form-control', 'id': 'tracking_no'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'id': 'price'}),
            'buyer': forms.Select(attrs={'class': 'form-control', 'id': 'buyer'}),
            'warehouse': forms.Select(attrs={'class': 'form-control', 'id': 'warehouse'}),
        }


PoProductFormset = modelformset_factory(
    PurchaseOrderProduct,
    fields=('brand', 'packing_type', 'canton', 'weight', 'wight', 'lenght', 'height', 'image', 'price', 'remark'),
    widgets={
        'brand': forms.TextInput(attrs={'class': 'form-control', 'id': 'brand'}),
        'packing_type': forms.TextInput(attrs={'class': 'form-control', 'id': 'packing_type'}),
        'canton': forms.NumberInput(attrs={'class': 'form-control', 'id': 'canton'}),
        'weight': forms.NumberInput(attrs={'class': 'form-control', 'id': 'weight'}),
        'wight': forms.NumberInput(attrs={'class': 'form-control', 'id': 'wight'}),
        'lenght': forms.NumberInput(attrs={'class': 'form-control', 'id': 'lenght'}),
        'height': forms.NumberInput(attrs={'class': 'form-control', 'id': 'height'}),
        'price': forms.NumberInput(attrs={'class': 'form-control', 'id': 'price'}),
        'image': forms.FileInput(attrs={'class': 'form-control', 'id': 'image'}),
        'remark': forms.TextInput(attrs={'class': 'form-control', 'id': 'po_number'}),
    }
)


# class PoProduct(forms.ModelForm):
#     class Meta:
#         model = PurchaseOrderProduct
#         fields = ['']
#
#         widgets = {
#             'po_number': forms.TextInput(attrs={'class': 'form-control', 'id': 'po_number'}),
#             'type': forms.TextInput(attrs={'class': 'form-control', 'id': 'type'}),
#             'is_paid': forms.CheckboxInput(attrs={'class': 'form-control', 'id': 'is_paid'}),
#             'shipping_by': forms.TextInput(attrs={'class': 'form-control', 'id': 'shipping_by'}),
#             'track_no': forms.TextInput(attrs={'class': 'form-control', 'id': 'tracking_no'}),
#             'price': forms.NumberInput(attrs={'class': 'form-control', 'id': 'price'}),
#             'buyer': forms.Select(attrs={'class': 'form-control', 'id': 'buyer'}),
#             'warehouse': forms.Select(attrs={'class': 'form-control', 'id': 'warehouse'}),
#         }

class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = ['name','status']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'name'}),
            'status': forms.Select(attrs={'class': 'form-control', 'id': 'status'}),
        }


PoFormset = modelformset_factory(PurchaseOrder,
                                 fields=('po_id',),
                                 widgets={
                                     'po_id': forms.Select(attrs={'class': 'form-control', 'id': 'po_id'})}
                                 )
