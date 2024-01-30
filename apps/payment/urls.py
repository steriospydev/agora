from django.urls import path
from  . import views

app_name = 'payment'

urlpatterns = [
      # payment
      path('', views.payment, name='payment'),        
      path('<str:id>/delete/', views.delete_payment,name='payment-delete'),
      path('<str:id>/update/', views.update_payment, name='payment-update'),

      # payee
      path('payee/', views.payee, name='payee'),
      path('payee/<str:id>/delete/', views.delete_payee,
            name='payee-delete'),
      path('payee/<str:payee_id>/update/', views.update_payee,
            name='payee-update'),
      # labels
      path('payee/labels/', views.payee_label,
            name='payee-label'),
      path('payee/labels/<str:id>/delete/', views.delete_payee_label,
            name='payee-label-delete'),
      # income
      path('source/', views.source, name='source'),
      path('source/<str:id>/delete/', views.delete_source,
            name='source-delete'),  
      path('income/', views.income, name='income'),
      path('income/<str:id>/delete/', views.delete_income,
          name='income-delete'),  
      # statistics
      path('statistics/', views.payment_statistics, name='statistics')
]