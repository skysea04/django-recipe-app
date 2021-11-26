from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
# Create your tests here.

class ModelTests(TestCase):
    
    def test_create_user_with_email_successful(self):
        # Test creating a new user with an email is successful
        email = 'test@skysea.com'
        password = 'test123456'
        user = get_user_model().objects.create_user(
            email=email, 
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
    
    def test_new_user_email_normalized(self):
        # Test the email for a new user is normalized
        email = 'test@SKYSEA.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_newuser_invalid_email(self):
        # Test creating user with no email raises error
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')
    
    def test_create_new_superuser(self):
        user = get_user_model().objects.create_superuser(
            'test@skysea.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email = 'admin@skysea.com',
            password = 'test123456'
        )

        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@skysea.com',
            password = 'test123456',
            name = 'test user full name'
        )

    def test_users_listed(self):
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)
        
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.admin_user.email)
