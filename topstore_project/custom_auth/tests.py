from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from basket.models import Basket
from custom_auth.models import Profile


class UserSignUpTestCase(APITestCase):

    def test_sign_up(self):
        """Test sign up view"""

        url = reverse('custom_auth:sign-up')
        data = {
            'username': 'TestUser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            User.objects
            .filter(username=data.get('username'))
            .exists()
        )

        user = User.objects.get(username=data.get('username'))

        self.assertTrue(
            Profile.objects
            .filter(user=user)
            .exists()
        )

        self.assertTrue(
            Basket.objects
            .filter(user=user)
            .exists()
        )


class AuthUserTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(
            username='TestUser23',
            password='testpass23'
        )

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def test_sign_in(self):
        """Test sign_in view"""

        url = reverse('custom_auth:sign-in')
        data = {
            'username': 'TestUser23',
            'password': 'testpass23'
        }
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sign_out(self):
        """Test sign_out"""

        self.client.login(
            username='TestUser23',
            password='testpass23'
        )
        url = reverse('custom_auth:sign-out')
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)


class ProfileTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(
            username='TestUser55',
            password='testpass555',
            first_name='Alex',
            last_name='Love',
            email='ex@ex.com'
        )
        Profile.objects.create(
            user_id=cls.user.pk,
            phone='+79991234455'
        )

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def test_get_profile(self):
        url = reverse('custom_auth:profile')
        response = self.client.get(url)

        self.assertEqual(
            response.status_code, status.HTTP_302_FOUND
        )

        self.client.login(
            username='TestUser55',
            password='testpass555'
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = {
            'full_name': 'Alex Love',
            'email': 'ex@ex.com',
            'phone': '+79991234455',
            'avatar': None
                }

        self.assertJSONEqual(response.content, expected_data)

    def test_update_profile(self):
        url = reverse('custom_auth:profile')
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        self.client.login(
            username='TestUser55',
            password='testpass555'
        )

        new_info = {
            'first_name': 'Bob',
            'last_name': 'Sun',
            'email': 'ex2@ex.com',
            'phone': '+79991231122',
        }
        response = self.client.post(url, data=new_info)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = {
            'full_name': 'Bob Sun',
            'email': 'ex2@ex.com',
            'phone': '+79991231122',
            'avatar': None
                }

        response = self.client.get(url)
        self.assertJSONEqual(response.content, expected_data)

        new_info = {
            'first_name': 'Nick',
            'phone': '+79998881122'
        }
        self.client.post(url, data=new_info)

        expected_data = {
            'full_name': 'Nick Sun',
            'email': 'ex2@ex.com',
            'phone': '+79998881122',
            'avatar': None
        }

        response = self.client.get(url)
        self.assertJSONEqual(response.content, expected_data)
