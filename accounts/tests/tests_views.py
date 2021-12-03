from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import User, Customer, Partner
from orders.models import ServiceType, Address
from rest_framework.authtoken.models import Token
from accounts.serializers import CustomerSerializer


class CustomerViewTest(APITestCase):
    def test_create_new_customer(self):
        """
        Teste para criação de um usuário customer
        """
        customer_data = {
            'username': 'john@mail.com',
            'email': 'john@mail.com',
            'password': '1234',            
            'full_name': 'John Field',
            'cpf': '888.888.888-88',
            'phone': '(21)97777-7777',
            'is_staff': True
        }
   
        response = self.client.post('/api/customers/', customer_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['email'], 'john@mail.com')
        self.assertEqual(response.json()['full_name'], 'John Field')
        self.assertEqual(response.json()['cpf'], '888.888.888-88')
        self.assertEqual(response.json()['phone'], '(21)97777-7777')
        self.assertNotIn('password', response.json())
        self.assertNotIn('username', response.json())
    
    
    def test_create_customer_fail_when_missing_fields(self):
        """
        Teste para criação falha por falta de campos de um usuário customer
        """
        customer_data = {
            'email': 'john@mail.com',
            'password': '1234',            
            'full_name': 'John Field',
        }
    
        response = self.client.post('/api/customers/', customer_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
    def test_create_customer_fail_when_cpf_exists(self):
        """
        Teste para criação falha por cpf já cadastrado
        """
        user = User.objects.create_user(
            username = 'john@mail.com',
            email = 'john@mail.com',
            password = '1234',
            full_name = 'Jonh Field',
            cpf = '888.888.888-88',
            phone = '(21)97777-7777',
            is_staff = True
        )

        Customer.objects.create(user_customer=user)

        customer_data = {
            'email': 'john@mail.com',
            'password': '1234',            
            'full_name': 'John Field',
            'cpf': '888.888.888-77',
            'phone': '(21)97777-8888',
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
            cpf = '888.888.888-88',
            phone = '(21)97777-7777',
            is_staff = True
        )

        Customer.objects.create(user_customer=user)

    
    def test_login_success(self):
        """
        Teste para login de usuário
        """
        login_data = {
            'email': 'john@mail.com',
            'password': '1234',
            'is_partner': False
        }
    
        response = self.client.post('/api/customers/login/', login_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.json())


    def test_login_fail(self):
        """
        Teste para login falho
        """
        login_data = {
            'email': 'john@mail.com',
            'password': '123',
            'is_partner': False           
        }
    
        response = self.client.post('/api/customers/login/', login_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SeachingAndUpdatingCustomerTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username = 'john@mail.com', password = '1234', email = 'john@mail.com', full_name = 'Jonh Field', cpf = '111.111.111-11', phone = '(21)99999-9999', is_staff = True)            
        self.customer = Customer.objects.create(user_customer=self.user)
        self.token = Token.objects.create(user=self.customer.user_customer)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}') 

            
    def test_anyone_authenticated_can_search_for_a_specific_customer_by_id(self):
        """
        Teste busca por customer específico por id necessita de autenticação
        """
        response = self.client.get(f'/api/customers/{self.customer.id}/', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CustomerSerializer(instance=self.customer).data, response.data)


    def test_is_is_not_possible_to_search_for_a_customer_by_id_that_does_not_exist(self): 
        """
        Teste busca falha por customer que não existe
        """
        response = self.client.get(f'/api/customers/{self.customer.id + 1}/', format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        

    def test_anonymous_cannot_search_for_a_specific_customer_by_id(self):
        """
        Teste busca por customer específico necessita de autenticação
        """
        self.client.force_authenticate(user=None)

        response = self.client.get(f'/api/customers/{self.customer.id}/', format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_only_the_customer_himself_can_update_his_data(self):
        """
        Teste apenas o próprio customer pode atualizar os próprios dados
        """
        customer_data = {
            'phone': '(11)98888-8888'
        }

        response = self.client.patch(f'/api/customers/{self.customer.id}/', customer_data, format='json')

        self.customer.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for k, v in customer_data.items():
            self.assertEquals(v, response.data[k])
            self.assertEquals(v, getattr(self.customer.user_customer, k))
        

    def test_is_is_not_possible_to_update_a_customer_by_id_that_does_not_exist(self):    
        """
        Teste atualização de dados de um customer inexistente deve falhar
        """    
        customer_data = {
            'phone': '(11)98888-8888'
        }

        response = self.client.patch(f'/api/customers/{self.customer.id + 1}/', customer_data, format='json')
        
        self.customer.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_a_customer_cannot_update_another_customer_data(self):
        """
        Teste busca por customer específico necessita de autenticação
        """
        user_2 = User.objects.create(username = 'johnteste2@mail.com', password = '1234', email = 'john2@mail.com', full_name = 'Jonh Field', cpf = '211.111.111-12', phone = '(11)99999-1111')            
        customer_2 = Customer.objects.create(user_customer=user_2)    

        customer_data = {
            'phone': '(11)98888-8881'
        }

        response = self.client.patch(f'/api/customers/{customer_2.id}/', customer_data, format='json')

        customer_2.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
                

class PartnerViewTest(APITestCase):

    def test_create_new_partner(self):
        """
        Teste criação de conta de partner
        """
        partner_data = {
            'username': 'john@mail.com',
            'email': 'john@mail.com',
            'password': '1234',            
            'full_name': 'John Field',
            'cpf': '111.111.111-11',
            'phone': '(11)99999-9999',
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
        self.assertEqual(response.json()['cpf'], '111.111.111-11')
        self.assertEqual(response.json()['phone'], '(11)99999-9999')
        self.assertEqual(response.json()['birthday'], '1999-01-01')
        self.assertEqual(response.json()['gender'], 'M')
        self.assertEqual(response.json()['describe'], 'Limpeza total em qualquer tipo de residência.')
        self.assertEqual(response.json()['service']['name'], 'Limpeza Residencial')
        self.assertEqual(response.json()['address']['place'], 'Rua das Araras')
        self.assertNotIn('password', response.json())
        self.assertNotIn('username', response.json())
    
    
    def test_create_partner_fail_when_missing_fields(self):
        """
        Teste criação de conta de partner deve falhar caso campos faltantes
        """
        customer_data = {
            'username': 'john@mail.com',
            'email': 'john@mail.com',
            'password': '1234',            
            'full_name': 'John Field',
            'phone': '(11)99998-9999',
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
        """
        Teste criação de conta de partner deve falhar caso cpf já esteja registrado.
        """
        user = User.objects.create_user(
            username = 'john2@mail.com',
            email = 'john2@mail.com',
            password = '1234',            
            full_name = 'John Field',
            cpf = '111.111.111-11',
            phone = '(41)99999-9998',
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
            'cpf': '111.111.111-11',
            'phone': '(51)99999-9998',
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
            cpf = '111.111.111-10',
            phone = '(51)99999-9998',
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
        """
        Teste login sucedido
        """
        login_data = {
            'email': 'john2@mail.com',
            'password': '1234',
            'is_partner': True
        }
    
        response = self.client.post('/api/partners/login/', login_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.json())


    def test_login_fail(self):
        """
        Teste login falho.
        """
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
            cpf = '111.111.111-11',
            phone = '(21)99999-9998',
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
        """
        Teste apenas o próprio partner pode atualizar os próprios dados
        """
        partner_data = {
            'phone': '(21)98888-8888',
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
        self.assertEqual(response.json()['phone'], '(21)98888-8888')
        self.assertEqual(response.json()['address']['place'], 'Rua das Pameiras')
                    

    def test_is_is_not_possible_to_update_a_partner_by_id_that_does_not_exist(self):
        """
        Teste é impossivel atualizar dados de um partner inexistente
        """
        partner_data = {
            'phone': '(21)98888-8888',
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
        """
        Teste é impossivel atualizar dados de um outro usuário
        """
        user_2 = User.objects.create_user(
            username = 'john2@mail.com',
            email = 'john2@mail.com',
            password = '1234',            
            full_name = 'John Field',
            cpf = '111.111.111-10',
            phone = '(11)99999-9990',
            is_staff = False
        )

        service_2 = ServiceType.objects.get(
            name = 'Passadoria'
        )

        partner_address_2 = Address.objects.create(
            place = 'Rua das Araras',
            number = '10',
            neighborhood = 'Vila Sul',
            complements = 'apt.104',
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
            'phone': '(21)98888-8888'
        }

        response = self.client.patch(f'/api/partners/{partner_2.id}/', partner_data, format='json')

        partner_2.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)