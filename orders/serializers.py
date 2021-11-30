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
