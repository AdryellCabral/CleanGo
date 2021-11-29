from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from accounts.serializers import UserSerializer, CustomerSerializer, UserUpdateSerializer
from accounts.models import User, Customer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db import IntegrityError


class AccountView(APIView):

    def post(self, request):

        data = request.data
        data['username'] = data['email']

        data_serializer = UserSerializer(data=request.data)
        if not data_serializer.is_valid():
            return Response(data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
               
        try:        
            new_user = User.objects.create_user(**data)
            new_customer = Customer.objects.create(user_customer=new_user)
            serialized = CustomerSerializer(new_customer)
            return Response(serialized.data['user_customer'], status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            return Response({'message': str(e)}, status=status.HTTP_409_CONFLICT)


class LoginView(APIView):

    def post(self, request):

        data = request.data

        try:
            username = data['email']
            password = data ['password']
        except KeyError:
            return Response({'message': 'You must inform the email and the password.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(
            username = data['email'],
            password = data ['password']
        )

        if user:
            token = Token.objects.get_or_create(user=user)[0]
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        
        return Response({'message': 'Email or password invalid.'}, status=status.HTTP_400_BAD_REQUEST)


class AccountByIdView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
       
    def get(self, request, customer_id=''):

        try:        
            customer = Customer.objects.get(id=customer_id)
            serialized = CustomerSerializer(customer)
            return Response(serialized.data['user_customer'], status=status.HTTP_200_OK)
        except:               
            return Response({'message': 'Invalid customer_id'}, status=status.HTTP_404_NOT_FOUND)


    def patch(self, request, customer_id=''):

        authenticated_customer = request.user
        update_data = request.data

        try:
            customer = User.objects.get(id=customer_id)                
        except:
            return Response({'message': 'Invalid customer_id'}, status=status.HTTP_404_NOT_FOUND)


        if authenticated_customer.id == customer.id:
            try:
                data_serializer = UserUpdateSerializer(customer, data=update_data)
                if not data_serializer.is_valid():
                    return Response(data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
                data_serializer.save()

                updated_customer = Customer.objects.get(id=customer_id)
                serialized = CustomerSerializer(updated_customer)

                return Response(serialized.data['user_customer'], status=status.HTTP_200_OK)
            except IntegrityError as e:
                return Response({'message': str(e)}, status=status.HTTP_409_CONFLICT)
        else:
            return Response({'message': 'You can update only your own data.'}, status=status.HTTP_403_FORBIDDEN)
          
