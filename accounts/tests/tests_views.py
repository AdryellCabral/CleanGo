from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import User, Customer, Partner
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
            'phone': '999999999'
        }
   
        response = self.client.post('/customers/', customer_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['email'], 'john@mail.com')
        self.assertEqual(response.json()['full_name'], 'John Field')
        self.assertEqual(response.json()['cpf'], '11111111111')
        self.assertEqual(response.json()['phone'], '999999999')
        self.assertNotIn('password', response.json())
        self.assertNotIn('username', response.json())
    
    
    def test_create_user_fail_when_missing_fields(self):
        customer_data_one = {
            'email': 'john@mail.com',
            'password': '1234',            
            'full_name': 'John Field',
        }
    
        response = self.client.post('/customers/', customer_data_one, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
    def test_create_user_fail_when_cpf_exists(self):
        user = User.objects.create_user(
            username = 'john@mail.com',
            email = 'john@mail.com',
            password = '1234',
            full_name = 'Jonh Field',
            cpf = '11111111111',
            phone = '999999999'
        )

        Customer.objects.create(user_customer=user)

        customer_data = {
            'email': 'john@mail.com',
            'password': '1234',            
            'full_name': 'John Field',
            'cpf': '11111111111',
            'phone': '888888888'
        }
    
        response = self.client.post('/customers/', customer_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)


class LoginViewTest(APITestCase):
    def setUp(self):
        user = User.objects.create_user(
            username = 'john@mail.com',
            email = 'john@mail.com',
            password = '1234',
            full_name = 'Jonh Field',
            cpf = '11111111111',
            phone = '999999999'
        )

        Customer.objects.create(user_customer=user)

    
    def test_login_success(self):
        login_data = {
            'email': 'john@mail.com',
            'password': '1234',
            'is_partner': False
        }
    
        response = self.client.post('/customers/login/', login_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.json())


    def test_login_fail(self):
        login_data = {
            'email': 'john@mail.com',
            'password': '123',
            'is_partner': False           
        }
    
        response = self.client.post('/customers/login/', login_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SeachingAndUpdatingCustomerTest(APITestCase):
    
    def test_anyone_authenticated_can_search_for_a_specific_customer_by_id(self):

        user = User.objects.create(username = 'john@mail.com', password = '1234', email = 'john@mail.com', full_name = 'Jonh Field', cpf = '11111111111', phone = '999999999')            
        customer = Customer.objects.create(user_customer=user)       
        
        token = Token.objects.create(user=customer.user_customer)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}') 

        response = self.client.get(f'/customers/{customer.user_customer.id}/', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CustomerSerializer(instance=customer).data['user_customer'], response.data)


    def test_is_is_not_possible_to_search_for_a_customer_by_id_that_does_not_exist(self): 

        user = User.objects.create(username = 'john@mail.com', password = '1234', email = 'john@mail.com', full_name = 'Jonh Field', cpf = '11111111111', phone = '999999999')            
        customer = Customer.objects.create(user_customer=user)       
        
        token = Token.objects.create(user=customer.user_customer)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')  

        response = self.client.get(f'/customers/{customer.user_customer.id + 1}/', format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        

    def test_anonymous_cannot_search_for_a_specific_customer_by_id(self):

        user = User.objects.create(username = 'john@mail.com', password = '1234', email = 'john@mail.com', full_name = 'Jonh Field', cpf = '11111111111', phone = '999999999')            
        customer = Customer.objects.create(user_customer=user)      

        response = self.client.get(f'/customers/{customer.user_customer.id}/', format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_only_the_customer_himself_can_update_his_data(self):

        user = User.objects.create(username = 'john@mail.com', password = '1234', email = 'john@mail.com', full_name = 'Jonh Field', cpf = '11111111111', phone = '999999999')            
        customer = Customer.objects.create(user_customer=user)       
        
        token = Token.objects.create(user=customer.user_customer)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')        
        
        self.client.login(email=customer.user_customer.email, password=customer.user_customer.email) 

        customer_data = {
            'phone': '888888888'
        }

        response = self.client.patch(f'/customers/{customer.user_customer.id}/', customer_data, format='json')

        customer.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for k, v in customer_data.items():
            self.assertEquals(v, response.data[k])
            self.assertEquals(v, getattr(customer.user_customer, k))
        

    def test_is_is_not_possible_to_update_a_customer_by_id_that_does_not_exist(self):
        
        user = User.objects.create(username = 'john@mail.com', password = '1234', email = 'john@mail.com', full_name = 'Jonh Field', cpf = '11111111111', phone = '999999999')            
        customer = Customer.objects.create(user_customer=user)       
        
        token = Token.objects.create(user=customer.user_customer)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')               
        
        self.client.login(email=customer.user_customer.email, password=customer.user_customer.email) 

        customer_data = {
            'phone': '888888888'
        }

        response = self.client.patch(f'/customers/{customer.user_customer.id + 1}/', customer_data, format='json')
        
        customer.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_a_user_cannot_update_another_user_data(self):

        user = User.objects.create(username = 'john@mail.com', password = '1234', email = 'john@mail.com', full_name = 'Jonh Field', cpf = '11111111111', phone = '999999999')            
        customer = Customer.objects.create(user_customer=user)       
        
        token = Token.objects.create(user=customer.user_customer)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}') 

        user_2 = User.objects.create(username = 'john2@mail.com', password = '1234', email = 'john2@mail.com', full_name = 'Jonh Field', cpf = '11111111112', phone = '999999998')            
        customer_2 = Customer.objects.create(user_customer=user_2)    

        self.client.login(email=customer.user_customer.email, password=customer.user_customer.email) 

        customer_data = {
            'phone': '888888888'
        }

        response = self.client.patch(f'/customers/{customer_2.user_customer.id}/', customer_data, format='json')

        customer.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
                
