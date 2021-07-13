from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('order/<int:id>/', views.order_detail, name="order"),
]
