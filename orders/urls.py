from django.urls import path
from .views import OrdersRetrieveUpdateDeleteView, OrdersView 

urlpatterns = [
    path('orders/', OrdersView.as_view()),
    path('orders/<int:order_id>', OrdersRetrieveUpdateDeleteView.as_view())
]