import os

import jwt
from django.test import TestCase, Client
from django.urls import reverse

from api.models import User


class TestUserAuth(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('token_obtain_pair')
        self.user_url = reverse('get_user')
        self.follow_url = reverse('follow_user')
        self.unfollow_url = reverse('unfollow_user')

        self.tuser1 = User.objects.create_user(email="testuser1@test.com", username="testuser1",
                                               password="testpassword1")
        self.tuser2 = User.objects.create_user(email="testuser2@test.com", username="testuser2",
                                               password="testpassword2")
        self.tuser3 = User.objects.create_user(email="testuser3@test.com", username="testuser3",
                                               password="testpassword3")
        self.tuser4 = User.objects.create_user(email="testuser4@test.com", username="testuser4",
                                               password="testpassword4")

    def test_user_login(self):
        response = self.client.post(self.login_url, {"email": self.tuser1.email, "password": "testpassword1"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.keys(), {"refresh", "access"})

        access_token = response.data['access']
        refresh_token = response.data['refresh']

        payload = jwt.decode(access_token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
        self.assertEqual(payload['username'], self.tuser1.username)
        self.assertEqual(payload['user_id'], self.tuser1.id)

    def test_user_login_invalid_field(self):
        response = self.client.post(self.login_url, {"email": self.tuser1.email, "password": "testpassword2"})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, {'detail': 'No active account found with the given credentials'})

    def test_user_login_missing_field(self):
        response = self.client.post(self.login_url, {"password": "testpassword1"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'email': ['This field is required.']})

        response = self.client.post(self.login_url, {"email": self.tuser1.email})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'password': ['This field is required.']})

    def test_get_user(self):
        response = self.client.post(self.login_url, {"email": self.tuser1.email, "password": "testpassword1"})
        access_token = response.data['access']

        response = self.client.get(self.user_url, HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.keys(), {"id", "username", "following", "followers"})
        self.assertEqual(response.data['id'], self.tuser1.id)
        self.assertEqual(response.data['username'], self.tuser1.username)
        self.assertEqual(response.data['following'], 0)
        self.assertEqual(response.data['followers'], 0)

    def test_get_user_invalid_token(self):
        response = self.client.get(self.user_url, HTTP_AUTHORIZATION=f'Bearer invalidtoken')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data.get('detail'), 'Given token not valid for any token type')

    def test_get_user_missing_token(self):
        response = self.client.get(self.user_url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data.get('detail'), 'Authentication credentials were not provided.')


class TestUserFollow(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('token_obtain_pair')
        self.user_url = reverse('get_user')
        self.follow_url = reverse('follow_user')
        self.unfollow_url = reverse('unfollow_user')

        self.tuser1 = User.objects.create_user(email="testuser1@test.com", username="testuser1",
                                               password="testpassword1")
        self.tuser2 = User.objects.create_user(email="testuser2@test.com", username="testuser2",
                                               password="testpassword2")
        self.tuser3 = User.objects.create_user(email="testuser3@test.com", username="testuser3",
                                               password="testpassword3")
        self.tuser4 = User.objects.create_user(email="testuser4@test.com", username="testuser4",
                                               password="testpassword4")

    def test_follow_user(self):
        response = self.client.post(self.login_url, {"email": self.tuser1.email, "password": "testpassword1"})
        access_token = response.data['access']

        response = self.client.post(f"{self.follow_url}{self.tuser2.id}/", HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'message': f'User {self.tuser2.username} followed successfully'})

        response = self.client.post(f"{self.follow_url}{self.tuser3.id}/", HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'message': f'User {self.tuser3.username} followed successfully'})

        response = self.client.get(self.user_url, HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['following'], 2)
        self.assertEqual(response.data['followers'], 0)

        response = self.client.post(self.login_url, {"email": self.tuser2.email, "password": "testpassword2"})
        access_token = response.data['access']

        response = self.client.get(self.user_url, HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['following'], 0)
        self.assertEqual(response.data['followers'], 1)

        response = self.client.post(self.login_url, {"email": self.tuser3.email, "password": "testpassword3"})
        access_token = response.data['access']

        response = self.client.get(self.user_url, HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['following'], 0)
        self.assertEqual(response.data['followers'], 1)

    def test_follow_user_invalid_id(self):
        response = self.client.post(self.login_url, {"email": self.tuser1.email, "password": "testpassword1"})
        access_token = response.data['access']

        response = self.client.post(f"{self.follow_url}8/", HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'message': 'User not found'})

        response = self.client.get(self.user_url, HTTP_AUTHORIZATION=f"Bearer {access_token}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['following'], 0)
        self.assertEqual(response.data['followers'], 0)

    def test_follow_user_missing_id(self):
        response = self.client.post(self.login_url, {"email": self.tuser1.email, "password": "testpassword1"})
        access_token = response.data['access']

        response = self.client.post(f"{self.follow_url}", HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'User id is required'})

        response = self.client.get(self.user_url, HTTP_AUTHORIZATION=f"Bearer {access_token}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['following'], 0)
        self.assertEqual(response.data['followers'], 0)

    def test_follow_user_already_following(self):
        response = self.client.post(self.login_url, {"email": self.tuser1.email, "password": "testpassword1"})
        access_token = response.data['access']
        self.client.post(f"{self.follow_url}{self.tuser2.id}/", HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = self.client.post(f"{self.follow_url}{self.tuser2.id}/", HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'You are already following this user'})

        response = self.client.get(self.user_url, HTTP_AUTHORIZATION=f"Bearer {access_token}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['following'], 1)
        self.assertEqual(response.data['followers'], 0)

    def test_follow_user_self(self):
        response = self.client.post(self.login_url, {"email": self.tuser1.email, "password": "testpassword1"})
        access_token = response.data['access']

        response = self.client.post(f"{self.follow_url}{self.tuser1.id}/", HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'You cannot follow yourself'})

        response = self.client.get(self.user_url, HTTP_AUTHORIZATION=f"Bearer {access_token}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['following'], 0)
        self.assertEqual(response.data['followers'], 0)

    def test_follow_user_invalid_token(self):
        response = self.client.post(f"{self.follow_url}{self.tuser2.id}/", HTTP_AUTHORIZATION=f"Bearer invalidtoken")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data.get('detail'), 'Given token not valid for any token type')

        response = self.client.post(self.login_url, {"email": self.tuser1.email, "password": "testpassword1"})
        access_token = response.data['access']

        response = self.client.get(self.user_url, HTTP_AUTHORIZATION=f"Bearer {access_token}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['following'], 0)
        self.assertEqual(response.data['followers'], 0)

    def test_follow_user_missing_token(self):
        response = self.client.post(f"{self.follow_url}{self.tuser2.id}/")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data.get('detail'), 'Authentication credentials were not provided.')

        response = self.client.post(self.login_url, {"email": self.tuser1.email, "password": "testpassword1"})
        access_token = response.data['access']

        response = self.client.get(self.user_url, HTTP_AUTHORIZATION=f"Bearer {access_token}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['following'], 0)
        self.assertEqual(response.data['followers'], 0)


class TestUserUnfollow(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('token_obtain_pair')
        self.user_url = reverse('get_user')
        self.unfollow_url = reverse('unfollow_user')

        self.tuser1 = User.objects.create_user(email="testuser1@test.com", username="testuser1",
                                               password="testpassword1")
        self.tuser2 = User.objects.create_user(email="testuser2@test.com", username="testuser2",
                                               password="testpassword2")
        self.tuser3 = User.objects.create_user(email="testuser3@test.com", username="testuser3",
                                               password="testpassword3")
        self.tuser4 = User.objects.create_user(email="testuser4@test.com", username="testuser4",
                                               password="testpassword4")

        self.tuser1.following.add(self.tuser2)
        self.tuser1.following.add(self.tuser3)

    def test_unfollow_user(self):
        response = self.client.post(self.login_url, {"email": self.tuser1.email, "password": "testpassword1"})
        access_token = response.data['access']

        response = self.client.post(f"{self.unfollow_url}{self.tuser2.id}/",
                                    HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': f"User {self.tuser2.username} unfollowed successfully"})

        response = self.client.get(self.user_url, HTTP_AUTHORIZATION=f"Bearer {access_token}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['following'], 1)
        self.assertEqual(response.data['followers'], 0)

    def test_unfollow_user_missing_id(self):
        response = self.client.post(self.login_url, {"email": self.tuser1.email, "password": "testpassword1"})
        access_token = response.data['access']

        response = self.client.post(f"{self.unfollow_url}", HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'User id is required'})

        response = self.client.get(self.user_url, HTTP_AUTHORIZATION=f"Bearer {access_token}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['following'], 2)
        self.assertEqual(response.data['followers'], 0)

    def test_unfollow_user_invalid_id(self):
        response = self.client.post(self.login_url, {"email": self.tuser1.email, "password": "testpassword1"})
        access_token = response.data['access']

        response = self.client.post(f"{self.unfollow_url}8/", HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'message': 'User not found'})

        response = self.client.get(self.user_url, HTTP_AUTHORIZATION=f"Bearer {access_token}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['following'], 2)
        self.assertEqual(response.data['followers'], 0)

    def test_unfollow_user_not_following(self):
        response = self.client.post(self.login_url, {"email": self.tuser1.email, "password": "testpassword1"})
        access_token = response.data['access']

        response = self.client.post(f"{self.unfollow_url}{self.tuser4.id}/", HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'You are not following this user'})

        response = self.client.get(self.user_url, HTTP_AUTHORIZATION=f"Bearer {access_token}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['following'], 2)
        self.assertEqual(response.data['followers'], 0)

    def test_unfollow_user_missing_token(self):
        response = self.client.post(f"{self.unfollow_url}{self.tuser2.id}/")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data.get('detail'), 'Authentication credentials were not provided.')

        response = self.client.post(self.login_url, {"email": self.tuser1.email, "password": "testpassword1"})
        access_token = response.data['access']

        response = self.client.get(self.user_url, HTTP_AUTHORIZATION=f"Bearer {access_token}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['following'], 2)
        self.assertEqual(response.data['followers'], 0)

    def test_unfollow_user_invalid_token(self):
        response = self.client.post(f"{self.unfollow_url}{self.tuser2.id}/", HTTP_AUTHORIZATION=f'Bearer 123')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data.get('detail'), 'Given token not valid for any token type')
