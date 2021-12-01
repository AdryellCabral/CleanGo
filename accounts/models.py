from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    full_name = models.CharField(max_length=255)
    cpf = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=50, unique=True)  


class Customer(models.Model):
    user_customer = models.OneToOneField('User', on_delete=models.CASCADE)


class Partner(models.Model):
    describe = models.CharField(max_length=255)
    gender = models.CharField(max_length=1)
    birthday = models.DateField()

    user_partner = models.OneToOneField('User', on_delete=models.CASCADE)

    service = models.ForeignKey('orders.ServiceType', on_delete=models.CASCADE, related_name='partners')
    address = models.ForeignKey('orders.Address', on_delete=models.CASCADE, related_name='partners')   



