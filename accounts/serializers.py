from rest_framework import serializers


class UserSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    full_name = serializers.CharField()
    cpf = serializers.CharField()
    phone = serializers.CharField()


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
    birthday = serializers.CharField()
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
    birthday = serializers.CharField()
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
        print(validated_data)
        print('teste')
        if validated_data.get('user_partner'):           
            instance.user_partner.username = validated_data.get('user_partner', instance.user_partner.username).get('username', instance.user_partner.username)
            instance.user_partner.email = validated_data.get('user_partner', instance.user_partner.email).get('email', instance.user_partner.email)
            instance.user_partner.password = validated_data.get('user_partner', instance.user_partner.password).get('password', instance.user_partner.password)
            instance.user_partner.full_name = validated_data.get('user_partner', instance.user_partner.full_name).get('full_name', instance.user_partner.full_name)
            instance.user_partner.cpf = validated_data.get('user_partner', instance.user_partner.cpf).get('cpf', instance.user_partner.cpf)
            instance.user_partner.phone = validated_data.get('user_partner', instance.user_partner.phone).get('phone', instance.user_partner.phone)
            instance.user_partner.save()
        
        if validated_data.get('address'):  
            instance.address.place = validated_data.get('address', instance.address.place).get('place', instance.address.place)
            instance.address.number = validated_data.get('address', instance.address.number).get('number', instance.address.number)
            instance.address.neighborhood = validated_data.get('address', instance.address.neighborhood).get('neighborhood', instance.address.neighborhood)
            instance.address.complements = validated_data.get('address', instance.address.complements).get('complements', instance.address.complements)
            instance.address.city = validated_data.get('address', instance.address.city).get('city', instance.address.city)
            instance.address.state = validated_data.get('address', instance.address.state).get('state', instance.address.state)
            instance.address.cep = validated_data.get('address', instance.address.cep).get('cep', instance.address.cep)
            instance.address.save()
        
        if validated_data.get('service'):  
            instance.service.name = validated_data.get('service', instance.service.name).get('name', instance.service.name)
            instance.service.save()

        instance.gender = validated_data.get('gender', instance.gender)
        instance.birthday = validated_data.get('birthday', instance.birthday)
        instance.describe = validated_data.get('describe', instance.describe)
        instance.save()              
        
        return instance

