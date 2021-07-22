from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from users.models import User
from .models import *
from .forms import *


# EMP views
@login_required(login_url='login')
def create_supplier(request):
    forms = EmployeeForm()
    if request.method == 'POST':
        forms = EmployeeForm(request.POST)
        if forms.is_valid():
            name = forms.cleaned_data['name']
            tel = forms.cleaned_data['tel']
            is_in_thai = forms.cleaned_data['is_in_thai']
            email = forms.cleaned_data['email']
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            retype_password = forms.cleaned_data['retype_password']
            if password == retype_password:
                if is_in_thai:
                    user = User.objects.create_user(username=username, password=password, email=email,
                                                    is_china=False)
                    Employee.objects.create(user=user, name=name, tel=tel,is_in_thai=True)
                else:
                    user = User.objects.create_user(username=username, password=password, email=email,
                                                    is_thai_inbound=False, is_thai_outbound=False)
                    Employee.objects.create(user=user, name=name, tel=tel, is_china=True)
                return redirect('supplier-list')
    context = {
        'form': forms
    }
    return render(request, 'store/addSupplier.html', context)


def show_all_emp(request):
    all_emp = Employee.objects.all()
    context = {'supplier':all_emp}
    return render(request,'store/supplier_list.html',context)

@login_required(login_url='login')
def delete_emp(request,emp_id):
    emp = Employee.objects.filter(id=emp_id).first()
    emp.delete()
    return HttpResponseRedirect("/store/supplier-list/")

@login_required(login_url='login')
def update_emp(request,emp_id):
    emp = Employee.objects.filter(id=emp_id).first()
    if emp == None:
        return HttpResponse("EMP_id "+str(emp_id) )
    context = {'emp':emp}
    return render(request,"store/editEmp.html",context)

def edit_emp(request):
    if request.method !="POST":
        return HttpResponse("Wrong Method")
    emp = Employee.objects.filter(id=request.POST.get('id')).first()
    if not emp:
        return HttpResponse("Not Found")
    emp.name = request.POST.get('name','')
    emp.tel = request.POST.get('tel','')
    emp.is_in_thai = request.POST.get('is_in_thai')
    if not emp.is_in_thai:
        emp.is_in_thai = False
    emp.is_in_china = request.POST.get('is_in_china')
    if not emp.is_in_china:
        emp.is_in_china = False
    emp.save()
    return HttpResponseRedirect("/store/supplier-list/")


# Buyer views
@login_required(login_url='login')
def create_buyer(request):
    forms = BuyerForm()
    if request.method == 'POST':
        forms = BuyerForm(request.POST)
        if forms.is_valid():
            name = forms.cleaned_data['name']
            address = forms.cleaned_data['address']
            email = forms.cleaned_data['email']
            line_id = forms.cleaned_data['line_id']
            tel = forms.cleaned_data['tel']
            zipcode = forms.cleaned_data['zipcode']
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            retype_password = forms.cleaned_data['retype_password']
            if password == retype_password:
                user = User.objects.create_user(username=username, password=password, email=email, is_buyer=True)
                Buyer.objects.create(user=user, name=name, address=address,line_id=line_id,tel=tel,zipcode=zipcode)
                return redirect('buyer-list')
    context = {
        'form': forms
    }
    return render(request, 'store/addbuyer.html', context)


def show_all_buyer(request):
    all_buyer = Buyer.objects.all()
    context = {'buyer':all_buyer}
    return render(request,'store/buyer_list.html',context)

@login_required(login_url='login')
def delete_buyer(request,buyer_id):
    buyer = Buyer.objects.filter(id=buyer_id).first()
    buyer.delete()
    return HttpResponseRedirect("/store/buyer-list/")


@login_required(login_url='login')
def update_buyer(request,buyer_id):
    buyer = Buyer.objects.filter(id=buyer_id).first()
    if buyer == None:
        return HttpResponse("Buyer_id "+str(buyer_id) )
    context = {'buyer':buyer}
    return render(request,"store/editBuyer.html",context)

def edit_buyer(request):
    if request.method !="POST":
        return HttpResponse("Wrong Method")
    print(request.POST.get('id'))
    buyer = Buyer.objects.filter(id=request.POST.get('id')).first()
    if not buyer:
        return HttpResponse("Not Found")
    buyer.name = request.POST.get('name','')
    buyer.address = request.POST.get('address','')
    buyer.email = request.POST.get('email','')
    buyer.client_id = request.POST.get('client_id','')
    buyer.line_id = request.POST.get('line_id','')
    buyer.tel = request.POST.get('tel','')
    buyer.zipcode = request.POST.get('zipcode','')
    buyer.save()
    return HttpResponseRedirect("/store/buyer-list/")




# Drop views
@login_required(login_url='login')
def create_drop(request):
    forms = DropForm()
    if request.method == 'POST':
        forms = DropForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('drop-list')
    context = {
        'form': forms
    }
    return render(request, 'store/addCategory.html', context)


class DropListView(ListView):
    model = Drop
    template_name = 'store/category_list.html'
    context_object_name = 'drop'


# Product views
@login_required(login_url='login')
def create_product(request):
    forms = ProductForm()
    if request.method == 'POST':
        forms = ProductForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('product-list')
    context = {
        'form': forms
    }
    return render(request, 'store/addProduct.html', context)


class ProductListView(ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'product'


# Order views
@login_required(login_url='login')
def create_order(request):
    forms = OrderForm()
    if request.method == 'POST':
        forms = OrderForm(request.POST)
        if forms.is_valid():
            supplier = forms.cleaned_data['supplier']
            product = forms.cleaned_data['product']
            design = forms.cleaned_data['design']
            color = forms.cleaned_data['color']
            buyer = forms.cleaned_data['buyer']
            season = forms.cleaned_data['season']
            drop = forms.cleaned_data['drop']
            Order.objects.create(
                supplier=supplier,
                product=product,
                design=design,
                color=color,
                buyer=buyer,
                season=season,
                drop=drop,
                status='pending'
            )
            return redirect('order-list')
    context = {
        'form': forms
    }
    return render(request, 'store/addOrder.html', context)


class OrderListView(ListView):
    model = Order
    template_name = 'store/order_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = Order.objects.all().order_by('-id')
        return context


# Delivery views
@login_required(login_url='login')
def create_delivery(request):
    forms = DeliveryForm()
    if request.method == 'POST':
        forms = DeliveryForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('delivery-list')
    context = {
        'form': forms
    }
    return render(request, 'store/addelivery.html', context)


class DeliveryListView(ListView):
    model = Delivery
    template_name = 'store/delivery_list.html'
    context_object_name = 'delivery'

@login_required(login_url='login')
def create_warehouse(request):
    forms = WarehouseForm()
    if request.method == 'POST':
        forms = WarehouseForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('warehouse-list')
    context = {
        'form': forms
    }
    return render(request, 'store/addWarehouse.html', context)


class WarehouseListView(ListView):
    model = Warehouse
    template_name = 'store/warehouse_list.html'
    context_object_name = 'warehouse'

#
def show_all_po(request):
    all_po = PurchaseOrder.objects.all()
    context = {'pos':all_po}
    return render(request,'store/po_list.html',context)


@login_required(login_url='login')
def create_po(request):
    forms = PoForm()
    if request.method == 'POST':
        forms = PoForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('po-list')
    context = {
        'form': forms
    }
    return render(request, 'store/addPo.html', context)

@login_required(login_url='login')
def update_po(request,po_id):
    po = PurchaseOrder.objects.filter(po_id=po_id).first()
    if po == None:
        return HttpResponse("po_id "+str(po_id) )
    context = {'po':po}
    return render(request,"store/editPo.html",context)

@login_required(login_url='login')
def edit_po(request,po_id):
    if request.method != "POST":
        return HttpResponse("Wrong Method")
    po = PurchaseOrder.objects.filter(po_id=request.POST.get('po_id')).first()
    if not po:
        return HttpResponse("Not Found")
    po.po_number = request.POST.get('po_number', '')
    po.type = request.POST.get('type', '')
    po.is_paid = request.POST.get('is_paid', '')
    po.shipping_by = request.POST.get('shipping_by', '')
    po.track_no = request.POST.get('track_no', '')
    po.price = request.POST.get('price', '')
    po.buyer = request.POST.get('buyer', '')
    po.warehouse = request.POST.get('warehouse', '')
    po.save()
    return HttpResponseRedirect("/store/po-list/")


@login_required(login_url='login')
def delete_po(request,po_id):
    obj = get_object_or_404(PurchaseOrder,po_id = po_id)
    if request.method == "GET":
        # delete object
        obj.delete()
        # after deleting redirect to
        # home page
    return redirect('po-list')
