from django.urls import path
from  . import views

app_name = 'supplier'

urlpatterns = [
    path('', views.supplier, name='supplier-list'),
    path('show/<str:id>/', views.supplier_detail, name='supplier-detail'),
    path('update/<str:id>', views.supplier_update, name='supplier-update'),

    path('shops/', views.shop, name='shop'),
    path('supplier-shop/connect/',
          views.connect_supplier_shop,
          name='supplier-shop-connect'),
    path('supplier-shop-delete/<str:shop_id>/',
          views.supplier_shop_delete,
            name='supplier-shop-delete'),
]