from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('', views.index, name="index"),
    path('add/', views.add_to_cart, name="add"),
    path('order/', views.create_order, name="order"),
    path('order-created/', views.order_created, name="order_created"),
]
