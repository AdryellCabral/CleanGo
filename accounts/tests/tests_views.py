from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import User, Customer, Partner
from orders.models import ServiceType, Address
from rest_framework.authtoken.models import Token
from accounts.serializers import CustomerSerializer


class CustomerViewTest(APITestCase):
    def test_create_new_customer(self):
        customer_data = {
            'username': 'john@mail.com',
            'email': 'john@mail.com',
            'password': '1234',            
            'full_name': 'John Field',
            'cpf': '11111111111',
            'phone': '999999999',
            'is_staff': True
        }
   
        response = self.client.post('/api/customers/', customer_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['email'], 'john@mail.com')
        self.assertEqual(response.json()['full_name'], 'John Field')
        self.assertEqual(response.json()['cpf'], '11111111111')
        self.assertEqual(response.json()['phone'], '999999999')
        self.assertNotIn('password', response.json())
        self.assertNotIn('username', response.json())
    
    
    def test_create_customer_fail_when_missing_fields(self):
        customer_data = {
            'email': 'john@mail.com',
            'password': '1234',            
            'full_name': 'John Field',
        }
    
        response = self.client.post('/api/customers/', customer_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
    def test_create_customer_fail_when_cpf_exists(self):
        user = User.objects.create_user(
            username = 'john@mail.com',
            email = 'john@mail.com',
            password = '1234',
            full_name = 'Jonh Field',
            cpf = '11111111111',
            phone = '999999999',
            is_staff = True
        )

        Customer.objects.create(user_customer=user)

        customer_data = {
            'email': 'john@mail.com',
            'password': '1234',            
            'full_name': 'John Field',
            'cpf': '11111111111',
            'phone': '888888888',
            'is_staff': True
        }
    
        response = self.client.post('/api/customers/', customer_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)


class LoginCustomerViewTest(APITestCase):
    def setUp(self):
        user = User.objects.create_user(
            username = 'john@mail.com',
            email = 'john@mail.com',
            password = '1234',
            full_name = 'Jonh Field',
            cpf = '11111111111',
            phone = '999999999',
            is_staff = True
        )

        Customer.objects.create(user_customer=user)

    
    def test_login_success(self):
        login_data = {
            'email': 'john@mail.com',
            'password': '1234',
            'is_partner': False
        }
    
        response = self.client.post('/api/customers/login/', login_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.json())


    def test_login_fail(self):
        login_data = {
            'email': 'john@mail.com',
            'password': '123',
            'is_partner': False           
        }
    
        response = self.client.post('/api/customers/login/', login_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SeachingAndUpdatingCustomerTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username = 'john@mail.com', password = '1234', email = 'john@mail.com', full_name = 'Jonh Field', cpf = '11111111111', phone = '999999999', is_staff = True)            
        self.customer = Customer.objects.create(user_customer=self.user)
        self.token = Token.objects.create(user=self.customer.user_customer)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}') 

            
    def test_anyone_authenticated_can_search_for_a_specific_customer_by_id(self):
        response = self.client.get(f'/api/customers/{self.customer.id}/', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CustomerSerializer(instance=self.customer).data, response.data)


    def test_is_is_not_possible_to_search_for_a_customer_by_id_that_does_not_exist(self): 
        response = self.client.get(f'/api/customers/{self.customer.id + 1}/', format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        

    def test_anonymous_cannot_search_for_a_specific_customer_by_id(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(f'/api/customers/{self.customer.id}/', format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_only_the_customer_himself_can_update_his_data(self):
        customer_data = {
            'phone': '888888888'
        }

        response = self.client.patch(f'/api/customers/{self.customer.id}/', customer_data, format='json')

        self.customer.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for k, v in customer_data.items():
            self.assertEquals(v, response.data[k])
            self.assertEquals(v, getattr(self.customer.user_customer, k))
        

    def test_is_is_not_possible_to_update_a_customer_by_id_that_does_not_exist(self):        
        customer_data = {
            'phone': '888888888'
        }

        response = self.client.patch(f'/api/customers/{self.customer.id + 1}/', customer_data, format='json')
        
        self.customer.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_a_customer_cannot_update_another_customer_data(self):
        user_2 = User.objects.create(username = 'johnteste2@mail.com', password = '1234', email = 'john2@mail.com', full_name = 'Jonh Field', cpf = '21111111112', phone = '9999999981')            
        customer_2 = Customer.objects.create(user_customer=user_2)    

        customer_data = {
            'phone': '8888888881'
        }

        response = self.client.patch(f'/api/customers/{customer_2.id}/', customer_data, format='json')

        customer_2.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
                

class PartnerViewTest(APITestCase):
    def setUp(self):
        ServiceType.objects.create(name='Limpeza Residencial')


    def test_create_new_partner(self):
        partner_data = {
            'username': 'john@mail.com',
            'email': 'john@mail.com',
            'password': '1234',            
            'full_name': 'John Field',
            'cpf': '11111111111',
            'phone': '999999999',
            'birthday': '1999-01-01',
            'gender': 'M',            
            'address':{
                'place': 'Rua das Araras',
                'number': '10',
                'neighborhood': 'Vila Norte',
                'complements': 'apt.102',
                'city': 'São Paulo',
                'state': 'SP',
                'cep': '82000000'
            },
            'services': 'Limpeza Residencial',
            'describe': 'Limpeza total em qualquer tipo de residência.',
            'is_staff': False
        }

        response = self.client.post('/api/partners/', partner_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['email'], 'john@mail.com')
        self.assertEqual(response.json()['full_name'], 'John Field')
        self.assertEqual(response.json()['cpf'], '11111111111')
        self.assertEqual(response.json()['phone'], '999999999')
        self.assertEqual(response.json()['birthday'], '1999-01-01')
        self.assertEqual(response.json()['gender'], 'M')
        self.assertEqual(response.json()['describe'], 'Limpeza total em qualquer tipo de residência.')
        self.assertEqual(response.json()['service']['name'], 'Limpeza Residencial')
        self.assertEqual(response.json()['address']['place'], 'Rua das Araras')
        self.assertNotIn('password', response.json())
        self.assertNotIn('username', response.json())
    
    
    def test_create_partner_fail_when_missing_fields(self):
        customer_data = {
            'username': 'john@mail.com',
            'email': 'john@mail.com',
            'password': '1234',            
            'full_name': 'John Field',
            'phone': '11999999999',
            'birthday': '1999-01-01',
            'gender': 'M',            
            'address':{
                'place': 'Rua das Araras',
                'number': '10',
                'neighborhood': 'Vila Norte',
                'complements': 'apt.102',
                'city': 'São Paulo',
                'state': 'SP',
                'cep': '82000000'
            },
            'services': 'Limpeza Residencial',
            'describe': 'Limpeza total em qualquer tipo de residência.',
            'is_staff': False
        }
    
        response = self.client.post('/api/partners/', customer_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
    def test_create_user_fail_when_cpf_exists(self):
        user = User.objects.create_user(
            username = 'john2@mail.com',
            email = 'john2@mail.com',
            password = '1234',            
            full_name = 'John Field',
            cpf = '11111111111',
            phone = '999999998',
            is_staff = False
        )

        service = ServiceType.objects.get(
            name = 'Limpeza Residencial'
        )

        partner_address = Address.objects.create(
            place = 'Rua das Araras',
            number = '10',
            neighborhood = 'Vila Norte',
            complements = 'apt.102',
            city = 'São Paulo',
            state = 'SP',
            cep = '82000000'
        )

        Partner.objects.create(
            user_partner = user,
            birthday = '1999-01-01',
            gender = 'M',
            describe = 'Limpeza total em qualquer tipo de residência.',
            service = service,
            address = partner_address 
        ) 

        partner_data = {
            'username': 'john2@mail.com',
            'email': 'john2@mail.com',
            'password': '1234',            
            'full_name': 'John Field',
            'cpf': '11111111111',
            'phone': '999999998',
            'birthday': '1999-01-01',
            'gender': 'M',            
            'address':{
                'place': 'Rua das Araras',
                'number': '10',
                'neighborhood': 'Vila Norte',
                'complements': 'apt.102',
                'city': 'São Paulo',
                'state': 'SP',
                'cep': '82000000'
            },
            'services': 'Limpeza Residencial',
            'describe': 'Limpeza total em qualquer tipo de residência.',
            'is_staff': False
        }
    
        response = self.client.post('/api/partners/', partner_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)


class LoginPartnerViewTest(APITestCase):
    def setUp(self):
        user = User.objects.create_user(
            username = 'john2@mail.com',
            email = 'john2@mail.com',
            password = '1234',            
            full_name = 'John Field',
            cpf = '11111111110',
            phone = '999999998',
            is_staff = False
        )

        service = ServiceType.objects.create(
            name = 'Limpeza Residencial'
        )

        partner_address = Address.objects.create(
            place = 'Rua das Araras',
            number = '10',
            neighborhood = 'Vila Norte',
            complements = 'apt.102',
            city = 'São Paulo',
            state = 'SP',
            cep = '82000000'
        )

        Partner.objects.create(
            user_partner = user,
            birthday = '1999-01-01',
            gender = 'M',
            describe = 'Limpeza total em qualquer tipo de residência.',
            service = service,
            address = partner_address 
        ) 
    

    def test_login_success(self):
        login_data = {
            'email': 'john2@mail.com',
            'password': '1234',
            'is_partner': True
        }
    
        response = self.client.post('/api/partners/login/', login_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.json())


    def test_login_fail(self):
        login_data = {
            'email': 'john2@mail.com',
            'password': '123',
            'is_partner': True           
        }
    
        response = self.client.post('/api/partners/login/', login_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdatingPartnerTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username = 'john@mail.com',
            email = 'john@mail.com',
            password = '1234',            
            full_name = 'John Field',
            cpf = '11111111111',
            phone = '999999998',
            is_staff = False
        )

        self.service = ServiceType.objects.create(
            name = 'Limpeza Residencial'
        )

        self.partner_address = Address.objects.create(
            place = 'Rua das Araras',
            number = '10',
            neighborhood = 'Vila Norte',
            complements = 'apt.102',
            city = 'São Paulo',
            state = 'SP',
            cep = '82000000'
        )

        self.partner = Partner.objects.create(
            user_partner = self.user,
            birthday = '1999-01-01',
            gender = 'M',
            describe = 'Limpeza total em qualquer tipo de residência.',
            service = self.service,
            address = self.partner_address 
        ) 
        
        self.token = Token.objects.create(user=self.partner.user_partner)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')


    def test_only_the_partner_himself_can_update_his_data(self):         
        partner_data = {
            'phone': '888888888',
            'address': {'place': 'Rua das Pameiras',
                        'number': '12',
                        'neighborhood': 'Vila Norte',
                        'complements': 'apt.704',
                        'city': 'São Paulo',
                        'state': 'SP',
                        'cep': '82100000'
                        }
        }

        response = self.client.patch(f'/api/partners/{self.partner.id}/', partner_data, format='json')

        self.partner.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['phone'], '888888888')
        self.assertEqual(response.json()['address']['place'], 'Rua das Pameiras')
                    

    def test_is_is_not_possible_to_update_a_partner_by_id_that_does_not_exist(self):        
        partner_data = {
            'phone': '888888888',
            'address': {'place': 'Rua das Pameiras',
                        'number': '12',
                        'neighborhood': 'Vila Norte',
                        'complements': 'apt.704',
                        'city': 'São Paulo',
                        'state': 'SP',
                        'cep': '82100000'
                        }
        }

        response = self.client.patch(f'/api/partners/{self.partner.id + 1}/', partner_data, format='json')
        
        self.partner.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_a_partner_cannot_update_another_user_data(self):
        user_2 = User.objects.create_user(
            username = 'john2@mail.com',
            email = 'john2@mail.com',
            password = '1234',            
            full_name = 'John Field',
            cpf = '11111111110',
            phone = '999999990',
            is_staff = False
        )

        service_2 = ServiceType.objects.create(
            name = 'Limpeza Residencial'
        )

        partner_address_2 = Address.objects.create(
            place = 'Rua das Araras',
            number = '10',
            neighborhood = 'Vila Norte',
            complements = 'apt.102',
            city = 'São Paulo',
            state = 'SP',
            cep = '82000000'
        )

        partner_2 = Partner.objects.create(
            user_partner = user_2,
            birthday = '1999-01-01',
            gender = 'M',
            describe = 'Limpeza total em qualquer tipo de residência.',
            service = service_2,
            address = partner_address_2 
        )     

        partner_data = {
            'phone': '888888888'
        }

        response = self.client.patch(f'/api/partners/{partner_2.id}/', partner_data, format='json')

        partner_2.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)