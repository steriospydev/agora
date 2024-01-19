from django.urls import path
from  . import views

app_name = 'product'

urlpatterns = [
    path('', views.product, name='product'),
    path('detail/<str:id>/', views.product_stats, name='stats'),
    path('delete/<str:id>/', views.delete_product, name='product-delete'),
    path('category/', views.category, name='category'),
    path('category/delete/<str:id>/', views.delete_category, name='category-delete'),
    path('variant/', views.variant, name='variant'),
    path('variant/delete/<str:id>/', views.delete_variant, name='variant-delete'),
    
]