from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from users.models import User
from .models import *
from .forms import *
from django.forms import inlineformset_factory


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
            client_id = forms.cleaned_data['client_id']
            line_id = forms.cleaned_data['line_id']
            tel = forms.cleaned_data['tel']
            zipcode = forms.cleaned_data['zipcode']
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            retype_password = forms.cleaned_data['retype_password']
            if password == retype_password:
                user = User.objects.create_user(username=username, password=password, email=email, is_buyer=True)
                Buyer.objects.create(user=user, name=name, address=address,line_id=line_id,tel=tel,zipcode=zipcode,client_id=client_id,email=email)
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
    all_po = PurchaseOrder.objects.all().order_by('-po_id')
    context = {'pos':all_po}
    return render(request,'store/po_list.html',context)

@login_required(login_url='login')
def create_po(request):
    template_name = 'store/addPo.html'
    if request.method == 'GET':
        poform = PoForm(request.GET or None)
        formset = PoProductFormset(queryset=PurchaseOrderProduct.objects.none())
    elif request.method == 'POST':
        poform = PoForm(request.POST)
        formset = PoProductFormset(request.POST,request.FILES)

        if poform.is_valid()and formset.is_valid():
            # first save this Po, as its reference will be used in `product`
            po = poform.save()
            for form in formset:
                # so that `book` instance can be attached.
                po_product = form.save(commit=False)
                po_product.po_id = po
                po_product.save()
            return redirect('po-list')
    return render(request, template_name, {
        'poform': poform,
        'formset': formset,
    })
@login_required(login_url='login')
def update_ship(request,ship_id):
    obj = Shipment.objects.get(id=ship_id)
    shipmentform = ShipmentForm(instance = obj)
    formset = PoFormset(queryset=PurchaseOrder.objects.filter(sack_id_id=ship_id))
    if shipmentform == None:
        return HttpResponse("Shipment "+str(ship_id) )
    if request.method == 'POST':
        data = request.POST
        obj.name = data['name']
        obj.status = data['status']
        obj.save()
        totalform = int(data['form-INITIAL_FORMS'])
        for number in range(totalform):
            sequence = 'form-'+str(number)+'-po_id'
            print(data[sequence])
            if data[sequence]:
                po = PurchaseOrder.objects.get(po_id=data[sequence])
                po.sack_id = obj
                po.save()

        return HttpResponseRedirect("/store/ship-list/")
    context = {
        'shipmentform':shipmentform,
        'formset':formset
    }
    return render(request,"store/editShipment.html",context)
@login_required(login_url='login')
def update_po(request,po_id):
    template_name = 'store/addPo.html'
    print(request.POST)
    obj = PurchaseOrder.objects.get(po_id=po_id)
    poform = PoForm(instance = obj)
    formset = PoProductFormset(queryset=PurchaseOrderProduct.objects.filter(po_id=po_id))
    if obj == None:
        return HttpResponse("po_id "+str(po_id) )
    if request.method == 'POST':
        data = request.POST
        print(data)
        buyer = Buyer.objects.get(id=int(data['buyer']))
        warehouse = Warehouse.objects.get(id=int(data['warehouse']))

        obj.po_number = data['po_number']
        obj.type = data['type']
        obj.is_paid = True if 'is_paid' in data else False
        obj.shipping_by = data['shipping_by']
        obj.track_no = data['track_no']
        obj.price = data['price']
        obj.buyer = buyer
        obj.warehouse = warehouse
        obj.save()
        totalform = int(data['form-INITIAL_FORMS'])

        for number in range(totalform):
            brand = 'form-' + str(number) + '-brand'
            packing_type = 'form-' + str(number) + '-packing_type'
            canton = 'form-' + str(number) + '-canton'
            weight = 'form-' + str(number) + '-weight'
            wight = 'form-' + str(number) + '-wight'
            lenght = 'form-' + str(number) + '-lenght'
            height = 'form-' + str(number) + '-height'
            price = 'form-' + str(number) + '-price'
            remark = 'form-' + str(number) + '-remark'
            image = 'form-' + str(number) + '-image'
            # pop = PurchaseOrderProduct.objects.get(po_id=data[sequence])
            # pop.sack_id = obj
            # pop.save()

    context ={
        'poform': poform,
        'formset': formset,
    }
    return render(request,template_name,context)

@login_required(login_url='login')
def edit_po(request):
    if request.method != "POST":
        return HttpResponse("Wrong Method")
    po = PurchaseOrder.objects.filter(po_id=request.POST.get('po_id')).first()
    if not po:
        return HttpResponse("Not Found")

    po.po_number = request.POST.get('po_number', '')
    po.type = request.POST.get('type', '')
    po.is_paid = request.POST.get('is_paid', False)
    po.shipping_by = request.POST.get('shipping_by', '')
    po.track_no = request.POST.get('track_no', '')
    po.price = request.POST.get('price', 0)
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

def show_all_shipment(request):
    all_po = Shipment.objects.all().order_by('-id')
    context = {'pos':all_po}
    return render(request,'store/shipment_list.html',context)

@login_required(login_url='login')
def create_shipment(request):
    template_name = 'store/addShipment.html'
    if request.method == 'GET':
        shipmentform = ShipmentForm(request.GET or None)
        formset = PoFormset(queryset=PurchaseOrder.objects.filter(sack_id__isnull=True))
    elif request.method == 'POST':
        shipmentform = ShipmentForm(request.POST)
        formset = PoFormset(request.POST)
        if shipmentform.is_valid()and formset.is_valid():
            shipment = shipmentform.save()
            for form in formset:
            # so that `book` instance can be attached.
                po = form.save(commit=False)
                po.sack_id = shipment
                if po.po_number:
                    po.save()


            return redirect('ship-list')
    return render(request, template_name, {
        'shipmentform': shipmentform,
        'formset': formset,
    })



@login_required(login_url='login')
def delete_ship(request,ship_id):
    obj = get_object_or_404(Shipment,id = ship_id)
    if request.method == "GET":
        # delete object
        obj.delete()
        # after deleting redirect to
        # home page
    return redirect('ship-list')