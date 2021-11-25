from django.test import TestCase
from accounts.models import User, Customer


class CustomerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.username = 'Customer'
        cls.password = '1234'
        cls.full_name = 'Jonh Field'
        cls.cpf = '11111111111'
        cls.phone = '999999999'     

        cls.user = User.objects.create_user(
            username=cls.username,
            password=cls.password,
            full_name=cls.full_name,
            cpf=cls.cpf,
            phone=cls.phone,
            is_partner=cls.is_partner
        )

        cls.customer = Customer.objects.create(
            user_customer=cls.user
        )

    def test_customer_fields(self):
        self.assertIsInstance(self.customer.user_customer, User)
        
        self.assertIsInstance(self.customer.user_customer.username, str)
        self.assertEqual(self.customer.customer_user.username, self.username)

        self.assertIsInstance(self.customer.user_customer.password, str)

        self.assertIsInstance(self.customer.user_customer.full_name, str)
        self.assertEqual(self.customer.user_customer.full_name, self.full_name)

        self.assertIsInstance(self.customer.user_customer.cpf, str)
        self.assertEqual(self.customer.user_customer.cpf, self.cpf)

        self.assertIsInstance(self.customer.user_customer.phone, str)
        self.assertEqual(self.customer.user_customer.phone, self.phone)