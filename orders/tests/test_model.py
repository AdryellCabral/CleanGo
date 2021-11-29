from django.test import TestCase
from datetime import date

from accounts.models import User,Customer
from ..models import Order,ServiceType,ResidenceType, Address

class TestOrderModel(TestCase):
    @classmethod
    def setUpTestData(cls):

        cls.user = User.objects.create(
            email="customer@email.com",
            password="1234",
            full_name="customer person",
            cpf="00000000000",
            phone="40028922"
        )

        cls.customer = Customer.objects.create(
            user_customer=cls.user
        )

        cls.serviceName = "Limpeza Residencial"

        cls.service = ServiceType.objects.create(
            name = cls.serviceName
        )

        cls.residenceName = "Casa"

        cls.residence = ResidenceType.objects.create(
            name = cls.residenceName
        )

        cls.place="Upton Forge",
        cls.number="t",
        cls.neighborhood="Account",
        cls.complements="fuchsia Applications TCP",
        cls.city="North Alberto",
        cls.state="SP",
        cls.cep=82000000

        cls.address = Address.objects.create(
            place=cls.place,
            number=cls.number,
            neighborhood=cls.neighborhood,
            complements=cls.complements,
            city=cls.city,
            state=cls.state,
            cep=cls.cep
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
            residences = cls.residenceType,
            service = cls.serviceType,
            opened = cls.opened,
            completed = cls.completed,
            address = cls.address
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

    def test_service_field_type(self):
        self.assertIsInstance(self.service.name, str)

    def test_service_field_value(self):
        self.assertEqual(self.service.name, self.serviceName)

    def test_residence_field_type(self):
        self.assertIsInstance(self.residence.name, str)

    def test_residence_field_value(self):
        self.assertEqual(self.residence.name, self.residenceName)

    def test_address_field_type(self):
        self.assertIsInstance(self.address.place, str)
        self.assertIsInstance(self.address.number, str)
        self.assertIsInstance(self.address.neighborhood, str)
        self.assertIsInstance(self.address.complements, str)
        self.assertIsInstance(self.address.city, str)
        self.assertIsInstance(self.address.state, str)
        self.assertIsInstance(self.address.cep, int)

    def test_address_field_value(self):
        self.assertEqual(self.address.place, self.place)
        self.assertEqual(self.address.number, self.number)
        self.assertEqual(self.address.neighborhood, self.neighborhood)
        self.assertEqual(self.address.complements, self.complements)
        self.assertEqual(self.address.city, self.city)
        self.assertEqual(self.address.state, self.state)
        self.assertEqual(self.address.cep, self.cep)