from django.urls import path
from  . import views

app_name = 'supplier'

urlpatterns = [
      path('', views.SupplierListView.as_view(), name='supplier-list'),
      path('shops/', views.ShopListView.as_view(), name='shop'),      
      path('update/<uuid:id>', views.SupplierUpdateView.as_view(), name='supplier-update'),
      
            
      path('supplier-shop/connect/',
            views.connect_supplier_shop,
            name='supplier-shop-connect'),
      path('supplier-shop-delete/<str:shop_id>/',
            views.SupplierShopDeleteView.as_view(),
                  name='supplier-shop-delete'),
      path('show/<str:id>/', views.supplier_detail, name='supplier-detail'),
]