from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from users.models import Follow
from django.urls import reverse
from django.core.cache import cache

class FollowUserTestCase(APITestCase):
    def setUp(self):
        # Reseta o rate limit
        cache.clear()
        # Criação de usuários de teste
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        self.followed_user = User.objects.create_user(username='followeduser', password='testpassword')

    def test_follow_user(self):
        """
        Testa a funcionalidade de seguir outro usuário.
        """
        url = reverse('follow', kwargs={'user_id': self.followed_user.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Follow.objects.count(), 1)
        self.assertEqual(Follow.objects.first().user, self.user)
        self.assertEqual(Follow.objects.first().followed_user, self.followed_user)

    def test_follow_user_twice(self):
        """
        Testa tentar seguir o mesmo usuário duas vezes.
        """
        url = reverse('follow', kwargs={'user_id': self.followed_user.id})
        self.client.post(url)  # Primeiro follow
        response = self.client.post(url)  # Tenta seguir de novo

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unfollow_user(self):
        """
        Testa a funcionalidade de deixar de seguir um usuário.
        """
        Follow.objects.create(user=self.user, followed_user=self.followed_user)
        url = reverse('unfollow', kwargs={'user_id': self.followed_user.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Follow.objects.count(), 0)

    def test_unfollow_user_not_following(self):
        """
        Testa tentar deixar de seguir um usuário quando não se está seguindo.
        """
        url = reverse('unfollow', kwargs={'user_id': self.followed_user.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserAuthTests(APITestCase):
    def setUp(self):
        # Reseta o rate limit
        cache.clear()

    def test_user_signup(self):
        """
        Testa se um novo usuário consegue se cadastrar.
        """
        url = reverse('signup')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword123'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().username, 'newuser')

    def test_user_login(self):
        """
        Testa se um usuário existente consegue fazer login e receber tokens JWT.
        """
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_wrong_credentials(self):
        """
        Testa tentativa de login com credenciais erradas.
        """
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

from decouple import config

class SignupRateLimitTest(APITestCase):

    def setUp(self):
        # Reseta o rate limit
        cache.clear()

        self.url = reverse('signup')

    def test_signup_rate_limit(self):
        # Tentar fazer 5 cadastros (sucesso)
        signupLimitPerHour = config("SIGNUP_LIMIT_PER_HOUR", cast=int)
        for i in range(signupLimitPerHour):
            data = {
                'username': f'user{i}',
                'email': f'user{i}@example.com',
                'password': 'password123'
            }
            response = self.client.post(self.url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Tentativa de cadastro excedendo o limite (deve retornar 429)
        data = {
            'username': 'userLimitExceeded',
            'email': 'userLimitExceeded@example.com',
            'password': 'password123'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class LoginRateLimitTest(APITestCase):

    def setUp(self):
        # Reseta o rate limit
        cache.clear()

        self.username = 'user'
        self.password = 'password123'
        User.objects.create_user(username=self.username, password=self.password)

        self.url = reverse('token_obtain_pair')

    def test_login_rate_limit(self):
        loginLimitPerHour = config("LOGIN_LIMIT_PER_HOUR", cast=int)
        data = {
            'username': self.username,
            'password': self.password
        }
        for i in range(loginLimitPerHour):
            response = self.client.post(self.url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class MeEndpointTest(APITestCase):
    def setUp(self):
        cache.clear()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_get_me_info(self):
        url = reverse('me')  # ajusta se o nome da rota for diferente
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')


from unittest.mock import patch
from users.tasks import send_new_follower_email
from django.test import TestCase

class SendFollowerEmailTest(TestCase):
    @patch('users.tasks.send_mail')
    def test_send_new_follower_email_task(self, mock_send_mail):
        # Chama a task diretamente (sem delay no teste)
        send_new_follower_email('follower@example.com', 'follower')

        # Verifica se o send_mail foi chamado uma vez
        self.assertTrue(mock_send_mail.called)
        self.assertEqual(mock_send_mail.call_count, 1)

        # Verifica se foi chamado com os argumentos corretos
        mock_send_mail.assert_called_with(
            'Novo seguidor no MiniTwitter!',
            'Você acabou de ganhar um novo seguidor: follower!',
            'no-reply@minitwitter.com',
            ['follower@example.com']
        )