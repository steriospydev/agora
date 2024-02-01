from django.urls import path
from  . import views

app_name = 'product'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product'),
    path('category/', views.CategoryListView.as_view(), name='category'),
    path('variant/', views.VariantListView.as_view(), name='variant'),    
    path('delete/<uuid:id>/',views.ProductDeleteView.as_view(), name='product-delete'),
    path('category/delete/<uuid:id>/', views.CategoryDeleteView.as_view(), name='category-delete'),
    path('variant/delete/<uuid:id>/', views.VariantDeleteView.as_view(), name='variant-delete'),
    path('detail/<uuid:pk>/', views.ProductStatsView.as_view(), name='stats'),
]