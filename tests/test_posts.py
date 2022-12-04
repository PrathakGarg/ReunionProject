import os

from django.test import TestCase, Client
from django.urls import reverse
import jwt

from api.models import Post, User


class CreatePostTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('token_obtain_pair')
        self.user_url = reverse('get_user')
        self.post_url = reverse('create_post')
        self.get_posts_url = reverse('get_posts')

        self.tester1 = User.objects.create_user(username='tester1', email='tester1@test.com', password='tester1')
        self.tester2 = User.objects.create_user(username='tester2', email='tester2@test.com', password='tester2')
        self.tester3 = User.objects.create_user(username='tester3', email='tester3@test.com', password='tester3')

        self.tester1.token = jwt.encode({'token_type': 'access',
                                         'exp': 9999999999,
                                         'iat': 0,
                                         'jti': '1234567890',
                                         'user_id': self.tester1.id,
                                         'username': self.tester1.username}, os.environ.get('SECRET_KEY'), algorithm='HS256')
        self.tester2.token = jwt.encode({'token_type': 'access',
                                            'exp': 9999999999,
                                            'iat': 0,
                                            'jti': '1234567890',
                                            'user_id': self.tester2.id,
                                            'username': self.tester2.username}, os.environ.get('SECRET_KEY'), algorithm='HS256')
        self.tester3.token = jwt.encode({'token_type': 'access',
                                            'exp': 9999999999,
                                            'iat': 0,
                                            'jti': '1234567890',
                                            'user_id': self.tester3.id,
                                            'username': self.tester3.username}, os.environ.get('SECRET_KEY'), algorithm='HS256')

    def test_create_post(self):
        response = self.client.post(self.post_url, {'title': "Test 1", 'desc': "Description 1"}, HTTP_AUTHORIZATION=f'Bearer {self.tester1.token}')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get('title'), "Test 1")
        self.assertEqual(response.data.get('desc'), "Description 1")
        self.assertEqual(response.data.get('id'), 1)

        response = self.client.get(self.get_posts_url, HTTP_AUTHORIZATION=f'Bearer {self.tester1.token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get('title'), "Test 1")
        self.assertEqual(response.data[0].get('desc'), "Description 1")
        self.assertEqual(response.data[0].get('id'), 1)

    def test_create_post_missing_fields(self):
        response = self.client.post(self.post_url, {'title': "Test 1"}, HTTP_AUTHORIZATION=f'Bearer {self.tester1.token}')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.get('errors').get("desc"), ['This field is required.'])

        response = self.client.post(self.post_url, {'desc': "Description 1"}, HTTP_AUTHORIZATION=f'Bearer {self.tester1.token}')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.get('errors').get("title"), ['This field is required.'])

        response = self.client.get(self.get_posts_url, HTTP_AUTHORIZATION=f'Bearer {self.tester1.token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_create_post_invalid_token(self):
        response = self.client.post(self.post_url, {'title': "Test 1", 'desc': "Description 1"}, HTTP_AUTHORIZATION=f'Bearer {self.tester1.token}invalid')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data.get('detail'), 'Given token not valid for any token type')

        response = self.client.get(self.get_posts_url, HTTP_AUTHORIZATION=f'Bearer {self.tester1.token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_create_post_missing_token(self):
        response = self.client.post(self.post_url, {'title': "Test 1", 'desc': "Description 1"})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data.get('detail'), 'Authentication credentials were not provided.')

        response = self.client.get(self.get_posts_url, HTTP_AUTHORIZATION=f'Bearer {self.tester1.token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)


class PostTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('token_obtain_pair')
        self.user_url = reverse('get_user')
        self.get_or_delete_post_url = lambda id: reverse('get_or_delete_post', args=[id])
        self.like_post_url = lambda id: reverse('like_post', args=[id])
        self.unlike_post_url = lambda id: reverse('unlike_post', args=[id])
        self.comment_post_url = lambda id: reverse('comment_post', args=[id])
        self.get_posts_url = reverse('get_posts')

        self.tester1 = User.objects.create_user(username='tester1', email='tester1@test.com', password='tester1')
        self.tester2 = User.objects.create_user(username='tester2', email='tester2@test.com', password='tester2')
        self.tester3 = User.objects.create_user(username='tester3', email='tester3@test.com', password='tester3')

        self.tester1.token = jwt.encode({'token_type': 'access',
                                         'exp': 9999999999,
                                         'iat': 0,
                                         'jti': '1234567890',
                                         'user_id': self.tester1.id,
                                         'username': self.tester1.username}, os.environ.get('SECRET_KEY'), algorithm='HS256')
        self.tester2.token = jwt.encode({'token_type': 'access',
                                            'exp': 9999999999,
                                            'iat': 0,
                                            'jti': '1234567890',
                                            'user_id': self.tester2.id,
                                            'username': self.tester2.username}, os.environ.get('SECRET_KEY'), algorithm='HS256')
        self.tester3.token = jwt.encode({'token_type': 'access',
                                            'exp': 9999999999,
                                            'iat': 0,
                                            'jti': '1234567890',
                                            'user_id': self.tester3.id,
                                            'username': self.tester3.username}, os.environ.get('SECRET_KEY'), algorithm='HS256')

        self.post1 = Post.objects.create(title="Test 1", desc="Description 1", user=self.tester1)
        self.post2 = Post.objects.create(title="Test 2", desc="Description 2", user=self.tester1)
        self.post3 = Post.objects.create(title="Test 3", desc="Description 3", user=self.tester2)

    def test_delete_post(self):
        response = self.client.delete(self.get_or_delete_post_url(self.post1.id), HTTP_AUTHORIZATION=f'Bearer {self.tester1.token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('message'), 'Post 1 deleted')

        response = self.client.get(self.get_posts_url, HTTP_AUTHORIZATION=f'Bearer {self.tester1.token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get('title'), "Test 2")
        self.assertEqual(response.data[0].get('desc'), "Description 2")

    def test_delete_post_invalid_id(self):
        response = self.client.delete(self.get_or_delete_post_url(999), HTTP_AUTHORIZATION=f'Bearer {self.tester1.token}')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data.get('message'), 'Post not found')

        response = self.client.get(self.get_posts_url, HTTP_AUTHORIZATION=f'Bearer {self.tester1.token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_delete_post_missing_token(self):
        response = self.client.delete(self.get_or_delete_post_url(self.post1.id))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data.get('detail'), 'Authentication credentials were not provided.')

        response = self.client.get(self.get_posts_url, HTTP_AUTHORIZATION=f'Bearer {self.tester1.token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_delete_post_invalid_token(self):
        response = self.client.delete(self.get_or_delete_post_url(self.post1.id), HTTP_AUTHORIZATION=f'Bearer {self.tester2.token}invalid')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data.get('detail'), 'Given token not valid for any token type')

        response = self.client.get(self.get_posts_url, HTTP_AUTHORIZATION=f'Bearer {self.tester1.token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_delete_post_unauthorized(self):
        response = self.client.delete(self.get_or_delete_post_url(self.post1.id), HTTP_AUTHORIZATION=f"Bearer {self.tester2.token}")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data.get('message'), 'You cannot delete this post')

        response = self.client.get(self.get_posts_url, HTTP_AUTHORIZATION=f'Bearer {self.tester1.token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_get_post(self):
        response = self.client.get(self.get_or_delete_post_url(self.post1.id), HTTP_AUTHORIZATION=f'Bearer {self.tester2.token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('title'), "Test 1")
        self.assertEqual(response.data.get('desc'), "Description 1")
        self.assertEqual(response.data.get('id'), self.post1.id)

    def test_get_post_invalid_id(self):
        response = self.client.get(self.get_or_delete_post_url(999), HTTP_AUTHORIZATION=f'Bearer {self.tester2.token}')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data.get('message'), 'Post not found')

    def test_get_post_missing_token(self):
        response = self.client.get(self.get_or_delete_post_url(self.post1.id))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data.get('detail'), 'Authentication credentials were not provided.')

    def test_get_post_invalid_token(self):
        response = self.client.get(self.get_or_delete_post_url(self.post1.id), HTTP_AUTHORIZATION=f'Bearer {self.tester2.token}invalid')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data.get('detail'), 'Given token not valid for any token type')

    def test_get_all_posts(self):
        response = self.client.get(self.get_posts_url, HTTP_AUTHORIZATION=f"Bearer {self.tester1.token}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0].get('title'), "Test 1")
        self.assertEqual(response.data[0].get('desc'), "Description 1")
        self.assertEqual(response.data[0].get('id'), self.post1.id)
        self.assertEqual(response.data[1].get('title'), "Test 2")
        self.assertEqual(response.data[1].get('desc'), "Description 2")
        self.assertEqual(response.data[1].get('id'), self.post2.id)

    def test_get_all_posts_missing_token(self):
        response = self.client.get(self.get_posts_url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data.get('detail'), 'Authentication credentials were not provided.')

    def test_get_all_posts_invalid_token(self):
        response = self.client.get(self.get_posts_url, HTTP_AUTHORIZATION=f'Bearer {self.tester1.token}invalid')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data.get('detail'), 'Given token not valid for any token type')

    def test_like_post(self):
        response = self.client.post(self.like_post_url(self.post1.id), HTTP_AUTHORIZATION=f"Bearer {self.tester2.token}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('message'), f'Post {self.post1.id} liked')

        response = self.client.get(self.get_posts_url, HTTP_AUTHORIZATION=f"Bearer {self.tester1.token}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0].get('likes'), 1)

    def test_like_post_invalid_id(self):
        response = self.client.post(self.like_post_url(999), HTTP_AUTHORIZATION=f"Bearer {self.tester2.token}")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data.get('message'), 'Post not found')

    def test_like_post_own_post(self):
        response = self.client.post(self.like_post_url(self.post1.id), HTTP_AUTHORIZATION=f"Bearer {self.tester1.token}")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.get('message'), 'You cannot like your own post')

        response = self.client.get(self.get_posts_url, HTTP_AUTHORIZATION=f"Bearer {self.tester1.token}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0].get('likes'), 0)

    def test_like_post_already_liked(self):
        response = self.client.post(self.like_post_url(self.post1.id), HTTP_AUTHORIZATION=f"Bearer {self.tester2.token}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('message'), f'Post {self.post1.id} liked')

        response = self.client.post(self.like_post_url(self.post1.id), HTTP_AUTHORIZATION=f"Bearer {self.tester2.token}")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.get('message'), 'You have already liked this post')

        response = self.client.get(self.get_posts_url, HTTP_AUTHORIZATION=f"Bearer {self.tester1.token}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0].get('likes'), 1)

    def test_like_post_missing_token(self):
        response = self.client.post(self.like_post_url(self.post1.id))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data.get('detail'), 'Authentication credentials were not provided.')

    def test_like_post_invalid_token(self):
        response = self.client.post(self.like_post_url(self.post1.id), HTTP_AUTHORIZATION=f'Bearer {self.tester1.token}invalid')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data.get('detail'), 'Given token not valid for any token type')

    def test_unlike_post(self):
        response = self.client.post(self.like_post_url(self.post1.id), HTTP_AUTHORIZATION=f"Bearer {self.tester2.token}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('message'), f'Post {self.post1.id} liked')

        response = self.client.post(self.unlike_post_url(self.post1.id), HTTP_AUTHORIZATION=f"Bearer {self.tester2.token}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('message'), f'Post {self.post1.id} unliked')

        response = self.client.get(self.get_posts_url, HTTP_AUTHORIZATION=f"Bearer {self.tester1.token}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0].get('likes'), 0)

    def test_unlike_post_invalid_id(self):
        response = self.client.post(self.unlike_post_url(999), HTTP_AUTHORIZATION=f"Bearer {self.tester2.token}")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data.get('message'), 'Post not found')

    def test_unlike_post_own_post(self):
        response = self.client.post(self.unlike_post_url(self.post1.id), HTTP_AUTHORIZATION=f"Bearer {self.tester1.token}")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.get('message'), 'You cannot unlike your own post')

    def test_unlike_post_not_liked(self):
        response = self.client.post(self.unlike_post_url(self.post1.id), HTTP_AUTHORIZATION=f"Bearer {self.tester2.token}")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.get('message'), 'You have not liked this post')

    def test_unlike_post_missing_token(self):
        response = self.client.post(self.unlike_post_url(self.post1.id))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data.get('detail'), 'Authentication credentials were not provided.')

    def test_unlike_post_invalid_token(self):
        response = self.client.post(self.unlike_post_url(self.post1.id), HTTP_AUTHORIZATION=f'Bearer {self.tester1.token}invalid')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data.get('detail'), 'Given token not valid for any token type')

    def test_comment_post(self):
        response = self.client.post(self.comment_post_url(self.post1.id), data={'comment': 'Test comment'}, HTTP_AUTHORIZATION=f"Bearer {self.tester2.token}")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get('cid'), 1)

        response = self.client.get(self.get_posts_url, HTTP_AUTHORIZATION=f"Bearer {self.tester1.token}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data[0].get('comments')), 1)
        self.assertEqual(response.data[0].get('comments')[0].get('comment'), 'Test comment')

    def test_comment_post_invalid_id(self):
        response = self.client.post(self.comment_post_url(999), data={'comment': 'Test comment'}, HTTP_AUTHORIZATION=f"Bearer {self.tester2.token}")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data.get('message'), 'Post not found')

    def test_comment_post_missing_comment(self):
        response = self.client.post(self.comment_post_url(self.post1.id), HTTP_AUTHORIZATION=f"Bearer {self.tester2.token}")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.get('errors').get("comment")[0], 'This field is required.')

    def test_comment_post_missing_token(self):
        response = self.client.post(self.comment_post_url(self.post1.id), data={'comment': 'Test comment'})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data.get('detail'), 'Authentication credentials were not provided.')

    def test_comment_post_invalid_token(self):
        response = self.client.post(self.comment_post_url(self.post1.id), data={'comment': 'Test comment'}, HTTP_AUTHORIZATION=f'Bearer {self.tester1.token}invalid')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data.get('detail'), 'Given token not valid for any token type')
