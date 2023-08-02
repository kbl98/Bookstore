
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import CustomUser
from rest_framework.test import APIClient
from .models import Book
from rest_framework.test import APITestCase

# Create your tests here.
class LoginTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpassword',
            author_pseudonym='pseudonym',
            email='testmail@mail.de'
        )
        self.token = Token.objects.create(user=self.user)
        

    def test_create_user(self):
        data = {
            'username': 'newuser',
            'password': 'newpassword',
            'author_pseudonym':'pseudonym',
            'email':'testmail@mail.de'
        }
        response = self.client.post('/users/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_all_users(self):
        self.admin_user = CustomUser.objects.create_user(
            username='adminuser',
            password='adminpassword',
            is_staff=True,
            is_superuser=True
        )
        self.admintoken=Token.objects.create(user=self.admin_user)
        self.client.defaults['HTTP_AUTHORIZATION'] = 'Token ' + self.admintoken.key
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_users_without_token(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    
    def test_login(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        response = self.client.post('/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_delete_user(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = 'Token ' + self.token.key
        response = self.client.delete(('/users/'+ str(self.user.id)+'/'))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CustomUser.objects.filter(pk=self.user.pk).exists())


class BookViewTests(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpassword',
            author_pseudonym='pseudonym',
            email='testmail@mail.de'
        )
        self.token = Token.objects.create(user=self.user)
        self.book = Book.objects.create(
            title='Test Book',
            description='This is a test book.',
            author=self.user,
            price='9.99'
        )

    def test_create_book(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = 'Token ' + self.token.key
        data = {
            'title':'Test Book',
            'description':'This is a test book.',
            'author':self.user.id,
            'price':'9.99'
        }
        response = self.client.post('/books/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
       
    
        


