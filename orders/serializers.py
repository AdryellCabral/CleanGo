from rest_framework import serializers
from accounts.serializers import CustomerSerializer 
# PartnerSerializer


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
    # partner = PartnerSerializer(allow_null=True)
    residence = ResidenceTypeSerializer(read_only=True)
    address = AddressSerializer(read_only=True)
    service = ServiceTypeSerializer(read_only=True)

    def update(self, instance, validated_data):
            instance.hours = validated_data.get('hours', instance.hours)
            instance.date = validated_data.get('date', instance.date)
            instance.bathrooms = validated_data.get('bathrooms', instance.bathrooms)
            instance.bedrooms = validated_data.get('bedrooms', instance.bedrooms)
            instance.value = validated_data.get('value', instance.value)
            instance.completed = validated_data.get('completed', instance.completed)
            instance.opened = validated_data.get('opened', instance.opened)
            # instance.partner = validated_data.get('partner', instance.partner)
            instance.residence = validated_data.get('residence', instance.residence)
            instance.address = validated_data.get('address', instance.address)
            instance.service = validated_data.get('service', instance.service)
            instance.save()
            return instance

