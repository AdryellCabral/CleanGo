from rest_framework import serializers
from orders.models import Address, ServiceType
from accounts.models import User
import re

class UserSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    full_name = serializers.CharField()
    cpf = serializers.CharField()
    phone = serializers.CharField()
    is_staff = serializers.BooleanField(write_only=True)
    
  
    # def validate(self, attrs):
    #     cpf = attrs['cpf']
    #     if re.fullmatch(r'^\[0-9]{3}\.?[0-9]{3}\.?[0-9]{3}\-?[0-9]{2}$', cpf) != None:
    #         return attrs                
    #     else:
    #         raise PhoneFormatError('Phone must be informed in the following format: (xx)9xxxx-xxxx.')


class CustomerSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(source='user_customer.email')    
    full_name = serializers.CharField(source='user_customer.full_name')
    cpf = serializers.CharField(source='user_customer.cpf')
    phone = serializers.CharField(source='user_customer.phone')


class CustomerUpdateSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(required=False, source='user_customer.username')
    email = serializers.EmailField(required=False, source='user_customer.email')
    password = serializers.CharField(required=False, source='user_customer.password')
    full_name = serializers.CharField(required=False, source='user_customer.full_name')
    cpf = serializers.CharField(required=False, source='user_customer.cpf')
    phone = serializers.CharField(required=False, source='user_customer.phone')

    
    def update(self, instance, validated_data):
        instance.user_customer.username = validated_data.get('user_customer', instance.user_customer.username).get('username', instance.user_customer.username)
        instance.user_customer.email = validated_data.get('user_customer', instance.user_customer.email).get('email', instance.user_customer.email)
        instance.user_customer.password = validated_data.get('user_customer', instance.user_customer.password).get('password', instance.user_customer.password)
        instance.user_customer.full_name = validated_data.get('user_customer', instance.user_customer.full_name).get('full_name', instance.user_customer.full_name)
        instance.user_customer.cpf = validated_data.get('user_customer', instance.user_customer.cpf).get('cpf', instance.user_customer.cpf)
        instance.user_customer.phone = validated_data.get('user_customer', instance.user_customer.phone).get('phone', instance.user_customer.phone)
        instance.user_customer.save()        
        return instance
 

class AddressPartnerSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    place = serializers.CharField()
    number = serializers.CharField()
    neighborhood = serializers.CharField()
    complements = serializers.CharField()
    city = serializers.CharField()
    state = serializers.CharField()
    cep = serializers.CharField()


class ServiceTypePartnerSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()


class PartnerCheckSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    user_partner = UserSerializer()
    birthday = serializers.DateField()
    gender = serializers.CharField()
    describe = serializers.CharField()
    service = ServiceTypePartnerSerializer()
    address = AddressPartnerSerializer()    
    describe = serializers.CharField()


class PartnerResponseSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(source='user_partner.email')    
    full_name = serializers.CharField(source='user_partner.full_name')
    cpf = serializers.CharField(source='user_partner.cpf')
    birthday = serializers.DateField()
    gender = serializers.CharField()
    phone = serializers.CharField(source='user_partner.phone')
    address = AddressPartnerSerializer()
    service = ServiceTypePartnerSerializer()    
    describe = serializers.CharField()


class PartnerUpdateSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(required=False, source='user_partner.username')
    email = serializers.EmailField(required=False, source='user_partner.email')
    password = serializers.CharField(required=False, source='user_partner.password')
    full_name = serializers.CharField(required=False, source='user_partner.full_name')
    cpf = serializers.CharField(required=False, source='user_partner.cpf')
    phone = serializers.CharField(required=False, source='user_partner.phone')
    gender = serializers.CharField(required=False)
    birthday = serializers.CharField(required=False)
    describe = serializers.CharField(required=False)
    services = ServiceTypePartnerSerializer(required=False)
    address = AddressPartnerSerializer(required=False)
   
    def update(self, instance, validated_data):

        if validated_data.get('user_partner'):           
            instance.user_partner.username = validated_data.get('user_partner', instance.user_partner.username).get('username', instance.user_partner.username)
            instance.user_partner.email = validated_data.get('user_partner', instance.user_partner.email).get('email', instance.user_partner.email)
            instance.user_partner.password = validated_data.get('user_partner', instance.user_partner.password).get('password', instance.user_partner.password)
            instance.user_partner.full_name = validated_data.get('user_partner', instance.user_partner.full_name).get('full_name', instance.user_partner.full_name)
            instance.user_partner.cpf = validated_data.get('user_partner', instance.user_partner.cpf).get('cpf', instance.user_partner.cpf)
            instance.user_partner.phone = validated_data.get('user_partner', instance.user_partner.phone).get('phone', instance.user_partner.phone)
            instance.user_partner.save()
        
        if validated_data.get('address'):
            new_address = Address.objects.get(**validated_data['address'])  
            instance.address = new_address
        
        if validated_data.get('service'):
            new_service = ServiceType.objects.get(**validated_data['service'])  
            instance.service = new_service

        instance.gender = validated_data.get('gender', instance.gender)
        instance.birthday = validated_data.get('birthday', instance.birthday)
        instance.describe = validated_data.get('describe', instance.describe)
        instance.save()              
        
        return instance

