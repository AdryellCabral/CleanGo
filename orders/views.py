from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import UserSerializer, CustomerSerializer 
from accounts.models import User, Customer, Partner
from orders.permissions import IsCustomerOrReadOnly
from orders.serializers import OrderSerializer, ServiceTypeSerializer, AddressSerializer, ResidenceTypeSerializer
from orders.models import Order, ServiceType, Address, ResidenceType
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import ipdb


class OrdersView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsCustomerOrReadOnly]

    def post(self, request):
        user = request.user
        request.data['partner'] = None
        data = request.data

        check_fields = ['residence', 'address', 'service']
        missing_fields = [item for item in check_fields if item not in data]
        if missing_fields:
            miss = str(missing_fields)[1:-1]
            return Response({'message': f'Missing fields: {miss}'}, status=status.HTTP_400_BAD_REQUEST)
                
        data_residence = data.pop('residence')
        data_address = data.pop('address')
        data_service = data.pop('service')

        residence = ResidenceType.objects.get(name=data_residence)
        service = ServiceType.objects.get(name=data_service)
        address = Address.objects.get_or_create(**data_address)
        data['residence'] = residence
        data['service'] = service
        data['address'] = address[0]

        data_serializer = OrderSerializer(data=data)
        if not data_serializer.is_valid():
            return Response(data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        customer = Customer.objects.get(user_customer=user)

        data['customer'] = customer
               
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

class OrdersRetrieveUpdateDeleteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsCustomerOrReadOnly]

    def patch(self, request,order_id):
        try:
            order = Order.objects.get(id=order_id)
            order_serializer = OrderSerializer(order,data=request.data,partial=True)
            if not order_serializer.is_valid():
                return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            order_serializer.save()

            return Response(order_serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"errors": "invalid order_id"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request,order_id):
        try:
            orders_list = Order.objects.get(id=order_id)
            serialized_list = OrderSerializer(orders_list, many=False)

            return Response(serialized_list.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"errors": "invalid order_id"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self,request, order_id=''):
        try:
            Order.objects.get(id=order_id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({"errors": "invalid order_id"}, status=status.HTTP_404_NOT_FOUND)