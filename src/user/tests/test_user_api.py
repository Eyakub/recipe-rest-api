from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """ test the users api (public) """

    def setup(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """ test creating user with valid payload is successful"""
        payload = {
            'email': 'test@eyakub.com',
            'password': 'testpass',
            'name': 'Test Eyakub'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        # self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """ Test creating a user that already exists fail"""
        payload = {'email': 'test@eyakub.com', 'password': 'testpass'}
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """ Test that the password must be more than five character"""
        payload = {
            'email': 'test@eyakub.com',
            'password': 'pw',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """ test that a token is created for the user """
        payload = {'email': 'test@eyakub.com', 'password': 'testpass'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """ test that token is not created if invalid credentials given """
        create_user(email='test@eyakub.com', password="testpass")
        payload = {'email': 'test@eyakub.com', 'password': 'wrong'}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """ test that token is not created if user doesn't exists """
        payload = {'email': 'test@eyakub.com', 'password': 'testpass'}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """ test that email and password are required """
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """ test that authentication is required for users """
        res = self.client.post(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """ Test API requests that require authentication """
    def setUp(self):
        self.user = create_user(
            email='test@eyakub.com',
            password='testpass',
            name='name',
        )
        self.client = APIClient()
        # force_authenticate is a helper function to authenticate our sample user
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile(self):
        """ Test retrieving profile for logged in user """
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # self.assertEqual(res.data, {
        #     'name': self.user.name,
        #     'email': self.user.email,
        # })

    def test_post_me_not_allowed(self):
        """ test that POST is not allowed on the ME url """
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """ test updating the user profile for authenticated user """
        payload = {'name': 'new name', 'password': 'newpassword'}
        res = self.client.patch(ME_URL, payload)

        # refresh from db helper function
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

