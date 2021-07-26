from django.urls import path

from .views import (
    create_supplier,
    create_buyer,
    create_drop,
    create_product,
    create_order,
    create_delivery,
    create_warehouse,
    create_po,
    create_shipment,


    show_all_emp,
    show_all_buyer,
    show_all_shipment,
    DropListView,
    ProductListView,
    OrderListView,
    DeliveryListView,
    WarehouseListView,
    show_all_po,

    update_buyer,
    update_emp,
    update_po,
    update_ship,

    edit_buyer,
    edit_emp,
    edit_po,

    delete_buyer,
    delete_emp,
    delete_po,
    delete_ship,

    change_status
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
    path('po-list/', show_all_po, name='po-list'),
    path('ship-list/', show_all_shipment, name='ship-list'),

    path('delete_buyer/<int:buyer_id>',delete_buyer, name='delete-buyer'),
    path('update_buyer/<int:buyer_id>',update_buyer, name='update-buyer'),
    path('edit_buyer', edit_buyer, name='edit-buyer'),

    path('delete_employee/<int:emp_id>', delete_emp, name='delete-emp'),
    path('update_employee/<int:emp_id>', update_emp, name='update-emp'),
    path('edit_emp', edit_emp, name='edit-emp'),

    path('create-po/', create_po, name='create-po'),
    path('delete_po/<int:po_id>', delete_po, name='delete-po'),
    path('update_po/<int:po_id>', update_po, name='update-po'),
    path('edit_po', edit_po, name='edit-po'),

    path('create-ship/', create_shipment, name='create-ship'),
    path('delete_ship/<int:ship_id>', delete_ship, name='delete-ship'),
    path('update_ship/<int:ship_id>', update_ship, name='update-ship'),

    path('scan-product/<int:qr_id>', change_status, name='scan-pro'),
]