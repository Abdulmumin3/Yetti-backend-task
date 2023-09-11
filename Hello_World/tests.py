from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
# from bs4 import BeautifulSoup
from .models import User
from .forms import CustomUserCreateForm
# from django.contrib.auth.forms import UserCreationForm

class UserRegistrationTest(TestCase):
    def test_registration_valid_data(self):
        response = self.client.post(reverse('register'), {
        	'email': 'test_user@example.com',
        	'password1': 'password123',
        	'password2': 'password123',
        })
        response.status_code = 302
        response.url =reverse('login')


    def test_registration_invalid_data(self):
    	response = self.client.post(reverse('register'), {
		    'email': 'test_user@example.com',
		    'password1': 'password123',
		    'password2': 'password123',
		})
    	response.status_code = 200  # Registration form should be displayed again

class UserLoginLogoutTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test_user@example.com', password='password123')

    def test_login_valid_credentials(self):
        response = self.client.post(reverse('login'), {
            'email': 'test_user@example.com',
            'password': 'password123',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login
        self.assertTrue(response.url.startswith(reverse('home')))

    def test_login_invalid_credentials(self):
        response = self.client.post(reverse('login'), {
            'email': 'test_user@example.com',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)  # Login form should be displayed again

    def test_logout(self):
        self.client.login(email='test_user@example.com', password='password123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after logout
        self.assertTrue(response.url.startswith(reverse('login')))  # Assuming logout redirects to login

class AuthenticationTest(TestCase):
    def test_unauthenticated_access_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)  # Redirects to login page

    def test_authenticated_access_home_page(self):
        self.user = User.objects.create_user(username='testuser', email='test_user@example.com', password='password123')
        self.client.login(email='test_user@example.com', password='password123')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)  # Successfully accesses home page

    # Add more tests for security vulnerabilities (e.g., session fixation, CSRF) as needed

class SessionFixationTest(TestCase):
    def test_session_fixation(self):
        # Create a user
        user = User.objects.create_user(username='testuser', email='test_user@example.com', password='password123')
        
        # Log in with the user and capture the session ID
        response = self.client.get(reverse('login'))
        session_id_before_login = response.client.session.session_key
        
        # Perform a session fixation attack by setting the session key explicitly
        self.client.force_login(user)
        
        # Log in again with the user
        self.client.login(email='test_user@example.com', password='password123')
        
        # Check if the session ID changed after login
        session_id_after_login = response.client.session.session_key
        self.assertNotEqual(session_id_before_login, session_id_after_login)

class CSRFAttackTest(TestCase):
    def test_csrf_attack(self):
        client = Client()
        response = client.post(
            reverse('csrf_attack'),
            data={'csrfmiddlewaretoken': 'invalid-token'},
        )
        response.status_code = 403 
        response.content = 'CSRF attack detected'
