from django.urls import path

from . import views

app_name = 'supplier-api'

urlpatterns = [
    path('all/',views.SupplierListView.as_view(),name='supplier-list'),
]