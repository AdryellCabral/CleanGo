from django.test import TestCase
from datetime import date

from accounts.models import User
from ..models import Order,ServiceType,ResidenceType

class TestOrderModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.customer = User.objects.create(
            email="customer@email.com",
            password="1234",
            full_name="customer person",
            cpf="00000000000",
            phone="40028922",
            is_partner=False
        )

        cls.customer = User.objects.create(
            email="customer@email.com",
            password="1234",
            full_name="customer person",
            cpf="00000000000",
            phone="40028922",
            is_partner=False
        )

        cls.serviceName = "Limpeza Residencial"

        cls.service = ServiceType.objects.create(
            name = cls.serviceName
        )

        cls.residenceName = "Casa"

        cls.residence = ResidenceType.objects.create(
            name = cls.residenceName
        )

        cls.hours = 2
        cls.date = date.fromisoformat("01/01/2030")
        cls.bathrooms = 2
        cls.bedrooms = 2
        cls.value = 200.00
        cls.opened = True,
        cls.completed = False,

        cls.order = Order.objects.create(
            hours = cls.hours,
            date = cls.date,
            bathrooms = cls.bathrooms,
            bedrooms = cls.bedrooms,
            value = cls.value,
            residence = cls.residenceType,
            service = cls.serviceType,
            opened = cls.opened,
            completed = cls.completed
        )

    def test_order_field_type(self):
        self.assertIsInstance(self.order.hours, int)
        self.assertIsInstance(self.order.date, date)
        self.assertIsInstance(self.order.bathrooms, int)
        self.assertIsInstance(self.order.bedrooms, int)
        self.assertIsInstance(self.order.value, float)
        self.assertIsInstance(self.order.opened, bool)
        self.assertIsInstance(self.order.completed, bool)
    
    def test_order_field_value(self):
        self.assertEqual(self.order.hours, self.hours)
        self.assertEqual(self.order.date, self.date)
        self.assertEqual(self.order.bathrooms, self.bathrooms)
        self.assertEqual(self.order.bedrooms, self.bedrooms)
        self.assertEqual(self.order.value, self.value)
        self.assertEqual(self.order.opened, self.opened)
        self.assertEqual(self.order.completed, self.completed)