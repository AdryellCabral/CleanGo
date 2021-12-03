from django.test import TestCase
from accounts.models import User, Customer, Partner
from orders.models import Address, ServiceType


class CustomerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.username = 'john@mail.com'
        cls.email = 'john@mail.com'
        cls.password = '1234'
        cls.full_name = 'Jonh Field'
        cls.cpf = '888.888.888-88'
        cls.phone = '(21)97777-7777'     

        cls.user = User.objects.create_user(
            username=cls.username,
            email=cls.email,
            password=cls.password,
            full_name=cls.full_name,
            cpf=cls.cpf,
            phone=cls.phone,
        )

        cls.customer = Customer.objects.create(
            user_customer=cls.user
        )

        cls.user_for_partner = User.objects.create(
            password="1234",
            full_name="John Wick Loves his dog",
            cpf = '888.888.888-99',
            phone = '(21)97777-8888'   
        )

        cls.service = ServiceType.objects.create(
            name="passar roupa"
        )

        cls.address = Address.objects.create(
            place="House",
            number="345",
            neighborhood="Parque das oliveiras",
            complements="You are beautyful",
            city="BHzada",
            state="Pão de queijo",
            cep="000000000000"
        )

        cls.partner = Partner.objects.create(
            user_partner=cls.user_for_partner,
            describe="Some description.",
            gender="F",
            birthday="1999-08-15",
            service=cls.service,
            address=cls.address
        )


    def test_customer_fields(self):
        """
        Teste para verificar os tipos e valores dos campos de customer
        """
        self.assertIsInstance(self.customer.user_customer, User)

        self.assertIsInstance(self.customer.user_customer.username, str)
        self.assertEqual(self.customer.user_customer.username, self.username)
        
        self.assertIsInstance(self.customer.user_customer.email, str)
        self.assertEqual(self.customer.user_customer.email, self.email)

        self.assertIsInstance(self.customer.user_customer.password, str)

        self.assertIsInstance(self.customer.user_customer.full_name, str)
        self.assertEqual(self.customer.user_customer.full_name, self.full_name)

        self.assertIsInstance(self.customer.user_customer.cpf, str)
        self.assertEqual(self.customer.user_customer.cpf, self.cpf)

        self.assertIsInstance(self.customer.user_customer.phone, str)
        self.assertEqual(self.customer.user_customer.phone, self.phone)

    def test_partner_table_fields(self):
        """
        Teste para verificar os tipos e valores dos campos de partner
        """

        partner = Partner.objects.get(id=self.partner.id)

        self.assertIsInstance(self.partner, Partner)

        self.assertIsInstance(self.partner.user_partner, User)

        self.assertIsInstance(self.partner.service, ServiceType)

        self.assertIsInstance(self.partner.address, Address)

        self.assertIsInstance(self.user_for_partner.full_name, str)
        self.assertEqual(self.user_for_partner.full_name, self.partner.user_partner.full_name)

        self.assertIsInstance(self.partner.id, int)
        self.assertEqual(self.partner.id, partner.id)

        self.assertIsInstance(self.partner.describe, str)
        self.assertEqual(self.partner.describe, partner.describe)

        self.assertIsInstance(self.partner.gender, str)
        self.assertEqual(self.partner.gender, partner.gender)

        self.assertIsInstance(self.partner.service.id, int)
        self.assertEqual(self.partner.service, self.service)

        self.assertIsInstance(self.partner.address.id, int)
        self.assertEqual(self.partner.address, self.address)



        