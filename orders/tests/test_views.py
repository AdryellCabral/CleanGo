from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from accounts.models import Customer, Partner
from ..models import (
    Order,
    Address,
    ResidenceType,
    ServiceType
)


class OrdersViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        customer_data = dict(
            full_name="Epchin Bot",
            email="epchinbot@teste.com",
            cpf="11542528330",
            password="123456",
            phone="45921541253"
        )

        partner_address_data = dict(
            place="Adeline Villages",
            number="5",
            neighborhood="Refined",
            complements="Fantastic Marketing Fresh Practical",
            city="Thaliachester",
            state="SP",
            cep="82000000"
        )

        customer_address_data = dict(
            place="Rua dos bots",
            number="123A",
            neighborhood="Bairro dos bots",
            complements="",
            city="Cidade dos bots",
            state="SP",
            cep="82000000"
        )

        cls.residence = ResidenceType.objects.create(dict(name='Casa'))
        cls.service = ServiceType.objects.create(
            dict(name="Limpeza Residencial")
        )
        cls.customer = Customer.objects.create(**customer_data)
        cls.partner_address = Address.objects.create(**partner_address_data)
        cls.customer_address = Address.objects.create(**customer_address_data)

        partner_data = dict(
            fullname='partner person',
            email='partner@email.com',
            password='1234',
            cpf='17203537510',
            birthday='01-01-1999',
            gender='F',
            phone='27999944920',
            address=cls.address,
            services=cls.service,
            describe="beatae nesciunt porro"
        )

        cls.partner = Partner.objects.create(**partner_data)

    def test_new_order_successful_created(self):

        order_data = dict(
            hours=2,
            date="01/01/2030",
            bathrooms=2,
            bedrooms=2,
            value=200.00,
            residence=self.residence,
            service=self.service,
            opened=True,
            completed=False,
            address=self.customer_address
        )

        customer_login_data = dict(
            email=self.customer.email,
            password=self.customer.password
        )

        token = Token.objects.get_or_create(user=customer_login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        response = self.client.post(
            '/api/orders/',
            order_data,
            format='json'
        )

        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(
            response.json(),
            dict(
                id=1,
                **order_data
            )
        )
