from django.urls import path
from .views import AccountView, LoginView, AccountByIdView 

urlpatterns = [
    path('customers/', AccountView.as_view()),
    path('customers/login/', LoginView.as_view()),
    path('customers/<int:customer_id>/', AccountByIdView.as_view()),
]