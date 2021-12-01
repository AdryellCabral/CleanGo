from rest_framework import serializers

class ResidenceTypeSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()


class AddressSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    place = serializers.CharField()
    number = serializers.CharField()
    neighborhood = serializers.CharField()
    complements = serializers.CharField()
    city = serializers.CharField()
    state = serializers.CharField()
    cep = serializers.CharField()


class ServiceTypeSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()

class PartnerSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(source='user_partner.email')    
    full_name = serializers.CharField(source='user_partner.full_name')
    cpf = serializers.CharField(source='user_partner.cpf')
    birthday = serializers.DateField()
    gender = serializers.CharField()
    phone = serializers.CharField(source='user_partner.phone')
    address = AddressSerializer()
    service = ServiceTypeSerializer()    
    describe = serializers.CharField()

class CustomerSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(source='user_customer.email')    
    full_name = serializers.CharField(source='user_customer.full_name')
    cpf = serializers.CharField(source='user_customer.cpf')
    phone = serializers.CharField(source='user_customer.phone')

class OrderSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    hours = serializers.IntegerField()
    date = serializers.DateField()
    bathrooms = serializers.IntegerField()
    bedrooms = serializers.IntegerField()
    value = serializers.FloatField()
    completed = serializers.BooleanField()
    opened = serializers.BooleanField()
    customer = CustomerSerializer(read_only=True)
    partner = PartnerSerializer(allow_null=True)
    residence = ResidenceTypeSerializer(read_only=True)
    address = AddressSerializer(read_only=True)
    service = ServiceTypeSerializer(read_only=True)

    def update(self, instance, validated_data):
            instance.completed = validated_data.get('completed', instance.completed)
            instance.opened = validated_data.get('opened', instance.opened)
            instance.save()
            return instance

