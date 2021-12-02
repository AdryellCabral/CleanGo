from django.db import models
from accounts.models import Customer, Partner

class ResidenceType(models.Model):
    name = models.CharField(max_length=50)

class Address(models.Model):
    place = models.CharField(max_length=50)
    number = models.CharField(max_length=10)
    neighborhood= models.CharField(max_length=50)
    complements= models.CharField(max_length=255, blank=True, null=True)
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    cep=models.CharField(max_length=50)

class ServiceType(models.Model):
    name = models.CharField(max_length=50)

class Order(models.Model):
    hours = models.IntegerField()
    date = models.DateField()
    bathrooms = models.IntegerField()
    bedrooms = models.IntegerField()
    value = models.FloatField()
    completed = models.BooleanField()
    opened = models.BooleanField()
    residence = models.ForeignKey(ResidenceType, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    service = models.ForeignKey(ServiceType, on_delete=models.CASCADE)

    # def __init__(self, id, hours, date, bathrooms, bedrooms, value, completed, opened, residence, customer, partner, address, service):
    #     self.id = id
    #     self.hours = hours
    #     self.date = date
    #     self.bathrooms = bathrooms
    #     self.bedrooms = bedrooms
    #     self.value = value
    #     self.completed = completed
    #     self.opened = opened
    #     self.residence = residence
    #     self.customer = customer
    #     self.partner = partner
    #     self.address = address
    #     self.service = service

