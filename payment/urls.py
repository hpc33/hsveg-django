from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('ecpay/', views.ecpay, name='ecpay',),
    path('process/', views.payment_process, name='process'),
    path('successful/', views.successful_payment, name='done'),
    path('canceled/', views.payment_canceled, name='canceled'),
]
