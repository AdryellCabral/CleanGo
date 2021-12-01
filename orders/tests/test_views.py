from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from accounts.models import Customer, Partner
from ..models import (
    Order,
    Address,
    ResidenceType,
    ServiceType
)


class TestOrdersView(APITestCase):
    """
    Esse é o teste para Views relacionadas a Order
    """
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

        cls.order_successful_data = dict(
            hours=2,
            date="01/01/2030",
            bathrooms=2,
            bedrooms=2,
            value=200.00,
            residence=cls.residence,
            service=cls.service,
            opened=True,
            completed=False,
            address=cls.customer_address
        )

        cls.order_without_fields_data = dict(
            hours=2,
            date="01/01/2030",
            bathrooms=2,
            bedrooms=2,
            value=200.00,
            residence=cls.residence,
            service=cls.service,
            opened=True,
            completed=False,
        )

        cls.customer_login_data = dict(
            email=cls.customer.email,
            password=cls.customer.password
        )

        cls.partner_login_data = dict(
            email=cls.partner.email,
            password=cls.partner.password
        )

    def test_only_customer_can_create_an_successful_order(self):
        """
        Aqui a criação de ordem será bem sucedida,
        criação sendo feito por um Customer.
        """

        # Simulando um login de customer.
        token, _ = Token.objects.get_or_create(user=self.customer_login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Fazendo a criação de uma ordem.
        response = self.client.post(
            '/api/orders/',
            self.order_successful_data,
            format='json'
        )

        # Fazendo o teste bem sucedido com a resposta da criação.
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(
            response.json(),
            dict(
                id=1,
                **self.order_successful_data
            )
        )

    def test_create_an_order_with_invalid_token(self):
        """
        Tentativa de criação com um token que
        não seja de um customer.
        """

        # Simulando um login de partner
        token, _ = Token.objects.get_or_create(user=self.partner_login_data)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        # Fazendo a criação de uma ordem.
        response = self.client.post(
            '/api/orders/',
            self.order_successful_data,
            format='json'
        )

        # Fazendo o teste mal sucedido com a resposta da criação.
        self.assertEqual(response.status_code, 403)
        self.assertDictEqual(
            response.json(),
            dict(
                detail="You do not have permission to perform this action."
            )
        )

    def test_create_an_order_without_fields(self):
        """
        Teste mal sucedido de criação de ordem sem algum campo.
        """

        # Simulando um login de customer.
        token, _ = Token.objects.get_or_create(user=self.customer_login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Fazendo a criação de uma ordem.
        response = self.client.post(
            '/api/orders/',
            self.order_successful_data,
            format='json'
        )

        # Fazendo o teste mal sucedido com a resposta da criação.
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(
            response.json(),
            dict(
                address=[
                    "This field is required."
                    ]
            )
        )

    def test_get_order_without_authentication(self):
        """
        Teste mal sucedido por não estar autenticado.
        """

        # Fazendo o request get de uma ordem.
        response = self.client.get(
            '/api/orders/',
            self.order_successful_data,
            format='json'
        )

        # Fazendo o teste mal sucedido com a resposta da criação.
        self.assertEqual(response.status_code, 401)
        self.assertDictEqual(
            response.json(),
            dict(
                detail="Authentication credentials were not provided."
            )
        )

    def test_get_order_successful_with_customer_authentication(self):
        """
        Teste de request get bem sucedido de ordem logado com customer.
        """

        # Simulando um login de customer.
        token, _ = Token.objects.get_or_create(user=self.customer_login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Fazendo a criação de uma ordem.
        response = self.client.post(
            '/api/orders/',
            self.order_successful_data,
            format='json'
        )

        # Fazendo o request get de uma ordem.
        response = self.client.get(
            '/api/orders/',
            self.order_successful_data,
            format='json'
        )

        # Fazendo o teste mal sucedido com a resposta da criação.
        self.assertEqual(response.status_code, 200)
        self.assertEquals(len(Order.object.all()), len(response.data))
        self.assertEqual(
            response.data[0].pop('id'),
            self.order_successful_data
        )

    def test_get_order_successful_with_partner_authentication(self):
        """
        Teste de request get bem sucedido de ordem logado com partner.
        """

        # Simulando um login de partner.
        token, _ = Token.objects.get_or_create(user=self.partner_login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Fazendo a criação de uma ordem.
        response = self.client.post(
            '/api/orders/',
            self.order_successful_data,
            format='json'
        )

        # Fazendo o request get de uma ordem.
        response = self.client.get(
            '/api/orders/',
            self.order_successful_data,
            format='json'
        )

        # Fazendo o teste mal sucedido com a resposta da criação.
        self.assertEqual(response.status_code, 200)
        self.assertEquals(len(Order.object.all()), len(response.data))
        self.assertEqual(
            response.data[0].pop('id'),
            self.order_successful_data
        )

    def test_get_order_by_id_unsuccessful_without_authentication(self):
        """
        Teste de request get por id da order sem autenticação.
        """

        # Fazendo o request get de uma ordem.
        response = self.client.get(
            '/api/orders/1',
            self.order_successful_data,
            format='json'
        )

        # Fazendo o teste mal sucedido com a resposta da criação.
        self.assertEqual(response.status_code, 401)
        self.assertDictEqual(
            response.json(),
            dict(
                detail="Authentication credentials were not provided."
            )
        )

    def test_get_order_by_id_successful_with_customer_authentication(self):
        """
        Teste de request get bem sucedido de ordem logado com customer.
        """

        # Simulando um login de customer.
        token, _ = Token.objects.get_or_create(user=self.customer_login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Fazendo a criação de uma ordem.
        response = self.client.post(
            '/api/orders/',
            self.order_successful_data,
            format='json'
        )

        # Fazendo o request get de uma ordem.
        response = self.client.get(
            '/api/orders/',
            self.order_successful_data,
            format='json'
        )

        # Fazendo o teste mal sucedido com a resposta da criação.
        self.assertEqual(response.status_code, 200)
        self.assertEquals(len(Order.object.all()), len(response.data))
        self.assertEqual(
            response.data[0].pop('id'),
            self.order_successful_data
        )

    def test_get_order_by_id_successful_with_partner_authentication(self):
        """
        Teste de request get bem sucedido de ordem logado com partner.
        """

        # Simulando um login de partner.
        token, _ = Token.objects.get_or_create(user=self.partner_login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Fazendo a criação de uma ordem.
        response = self.client.post(
            '/api/orders/',
            self.order_successful_data,
            format='json'
        )

        # Fazendo o request get de uma ordem.
        response = self.client.get(
            '/api/orders/',
            self.order_successful_data,
            format='json'
        )

        # Fazendo o teste mal sucedido com a resposta da criação.
        self.assertEqual(response.status_code, 200)
        self.assertEquals(len(Order.object.all()), len(response.data))
        self.assertEqual(
            response.data[0].pop('id'),
            self.order_successful_data
        )

    def test_order_accepted_by_partner_and_completed_by_customer(self):
        """
        teste de update para aceitar a ordem e completa-la
        """

        # Simulando um login de customer.
        token, _ = Token.objects.get_or_create(user=self.customer_login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Fazendo a criação de uma ordem.
        new_order = self.client.post(
            '/api/orders/',
            self.order_successful_data,
            format='json'
        )

        # Simulando um login de partner.
        token, _ = Token.objects.get_or_create(user=self.partner_login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Fazendo o request path para aceitar a ordem.
        response = self.client.patch(
            f'/api/orders/{new_order.id}',
            dict(opened=False),
            format='json'
        )

        # Fazendo update direto no banco.
        new_order.refresh_from_db()

         # Simulando um login de customer.
        token, _ = Token.objects.get_or_create(user=self.customer_login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Fazendo o request path para completar a ordem.
        response = self.client.patch(
            f'/api/orders/{new_order.id}',
            dict(completed=True),
            format='json'
        )

        # Fazendo os testes de aceite da ordem.
        self.assertEquals(200, response.status_code)
        self.assertEquals(False, response.opened)
        self.assertEquals(True, response.completed)

    def test_unsuccessful_order_accept_by_customer(self):
        """
        teste de update para aceitar a ordem com usuário customer
        """

        # Simulando um login de customer.
        token, _ = Token.objects.get_or_create(user=self.customer_login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Fazendo a criação de uma ordem.
        new_order = self.client.post(
            '/api/orders/',
            self.order_successful_data,
            format='json'
        )

        # Simulando um login de customer.
        token, _ = Token.objects.get_or_create(user=self.customer_login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Fazendo o request path da order.
        response = self.client.patch(
            f'/api/orders/{new_order.id}',
            dict(opened=False),
            format='json'
        )

        # Fazendo os testes de aceite da ordem
        self.assertEquals(400, response.status_code)

    def test_unsuccessful_order_accept_by_anonymous(self):
        """
        teste de update para aceitar a ordem com o usuário anônimo
        """

        # Simulando um login de customer.
        token, _ = Token.objects.get_or_create(user=self.customer_login_data)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Fazendo a criação de uma ordem.
        new_order = self.client.post(
            '/api/orders/',
            self.order_successful_data,
            format='json'
        )

        # Simulando um anônimo.
        self.client.credentials()

        # Fazendo o request path da order.
        response = self.client.patch(
            f'/api/orders/{new_order.id}',
            dict(opened=False),
            format='json'
        )

        # Fazendo os testes de aceite da ordem
        self.assertEquals(400, response.status_code)
