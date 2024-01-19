from django.urls import path
from  . import views

app_name = 'order'

urlpatterns = [
    path('', views.order, name='order-list'),
    path('delete/<str:id>/', views.delete_order, name='order-delete'),
    path('details/<str:id>/', views.detail_order, name='order-detail'),
    path('<str:order_id>/add_costs/', views.update_order, name='order-update'),
    path('<str:order_id>/add_product/', views.add_product, name='add-product'),
    path('<str:item_id>/update_product/', views.update_order_item, name='update-product'),
    path('<str:order_id>/remove_product/<str:id>',
          views.remove_product, name='remove-product')
]