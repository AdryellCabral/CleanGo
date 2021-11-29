from rest_framework import serializers
from accounts.models import User, Customer


class UserSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    full_name = serializers.CharField()
    cpf = serializers.CharField()
    phone = serializers.CharField()


class CustomerSerializer(serializers.Serializer):

    user_customer = UserSerializer()


class UserUpdateSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(required=False)
    full_name = serializers.CharField(required=False)
    cpf = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)

    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('email', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.cpf = validated_data.get('cpf', instance.cpf)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
        return instance
 