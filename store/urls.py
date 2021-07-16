from django.urls import path

from .views import (
    create_supplier,
    create_buyer,
    create_drop,
    create_product,
    create_order,
    create_delivery,
    create_warehouse,

    show_all_emp,
    show_all_buyer,
    DropListView,
    ProductListView,
    OrderListView,
    DeliveryListView,
    WarehouseListView,

    update_buyer,
    update_emp,

    edit_buyer,
    edit_emp,

    delete_buyer,
    delete_emp
)

urlpatterns = [
    path('create-supplier/', create_supplier, name='create-supplier'),
    path('create-buyer/', create_buyer, name='create-buyer'),
    path('create-drop/', create_drop, name='create-drop'),
    path('create-product/', create_product, name='create-product'),
    path('create-order/', create_order, name='create-order'),
    path('create-delivery/', create_delivery, name='create-delivery'),
    path('create-warehouse/', create_warehouse, name='create-warehouse'),

    path('supplier-list/', show_all_emp, name='supplier-list'),
    path('buyer-list/', show_all_buyer, name='buyer-list'),
    path('drop-list/', DropListView.as_view(), name='drop-list'),
    path('product-list/', ProductListView.as_view(), name='product-list'),
    path('order-list/', OrderListView.as_view(), name='order-list'),
    path('delivery-list/', DeliveryListView.as_view(), name='delivery-list'),
    path('warehouse-list/', WarehouseListView.as_view(), name='warehouse-list'),

    path('delete_buyer/<int:buyer_id>',delete_buyer, name='delete-buyer'),
    path('update_buyer/<int:buyer_id>',update_buyer, name='update-buyer'),
    path('edit_buyer', edit_buyer, name='edit-buyer'),

    path('delete_employee/<int:emp_id>', delete_emp, name='delete-emp'),
    path('update_employee/<int:emp_id>', update_emp, name='update-emp'),
    path('edit_emp', edit_emp, name='edit-emp'),

]