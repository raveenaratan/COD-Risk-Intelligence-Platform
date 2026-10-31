from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('orders/', views.orders_list, name='orders'),

    path(
        'order/<str:order_id>/',
        views.order_detail,
        name='order_detail'
    ),

    path('analytics/', views.analytics, name='analytics'),

    path('predict/', views.predict, name='predict'),

    path('founder/', views.founder, name='founder'),

    path(
    'whatsapp/',
    views.whatsapp_simulator,
    name='whatsapp_simulator'
),

    path(
    "customer/<str:name>/",
    views.customer_history,
    name="customer_history"
),

    path(
    'pincode/<str:pincode>/',
    views.pincode_detail,
    name='pincode_detail'
),

    path(
    'courier/<str:courier>/',
    views.courier_detail,
    name='courier_detail'
),


]
