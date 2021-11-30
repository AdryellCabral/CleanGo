from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import UserSerializer, CustomerSerializer 
from accounts.models import User, Customer, Partner
from orders.serializers import OrderSerializer, ServiceTypeSerializer, AddressSerializer, ResidenceTypeSerializer
from orders.models import Order, ServiceType, Address, ResidenceType
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db import IntegrityError


class OrdersView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        data = request.data
        data_residence = data.pop('residence')
        data_address = data.pop('address')
        data_service = data.pop('service')

        data_serializer = OrderSerializer(data=request.data)
        if not data_serializer.is_valid():
            return Response(data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        customer = Customer.objects.get(user_customer=user)
        residence = ResidenceType.objects.get(name=data_residence)
        service = ServiceType.objects.get(name=data_service)
        address = Address.objects.get_or_create(**data_address)

        data['customer'] = customer
        data['residence'] = residence
        data['service'] = service
        data['address'] = address[0]         
               
        try:        
            new_order = Order.objects.create(**data)
            serialized = OrderSerializer(new_order)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            return Response({'message': str(e)}, status=status.HTTP_409_CONFLICT)


    def get(self, request):            
            orders_list = Order.objects.all()
            serialized_list = OrderSerializer(orders_list, many=True)
  
            return Response(serialized_list.data, status=status.HTTP_200_OK)       
               
     