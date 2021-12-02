from django.urls import path
from .views import AccountCustomerView, LoginCustomerView, AccountCustomerByIdView,\
     AccountPartnerView, LoginPartnerView, AccountPartnerByIdView 


urlpatterns = [
    path('customers/', AccountCustomerView.as_view()),
    path('partners/', AccountPartnerView.as_view()),
    path('customers/login/', LoginCustomerView.as_view()),
    path('partners/login/', LoginPartnerView.as_view()),
    path('customers/<int:customer_id>/', AccountCustomerByIdView.as_view()),
    path('partners/<int:customer_id>/', AccountPartnerByIdView.as_view()),
]