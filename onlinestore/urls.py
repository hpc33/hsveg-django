from unicodedata import name
from xml.etree.ElementInclude import include
from django.urls import path
from . import views

app_name = 'onlinestore'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    # path('payment/', include(('payment.urls', 'payment'), name='payment')),
]
