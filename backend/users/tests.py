from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.urls import reverse
from users.models import Follow
User = get_user_model()

class FollowUserTestCase(APITestCase):
    def setUp(self):
        # Reseta o rate limit
        cache.clear()
        # Criação de usuários de teste
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.force_authenticate(user=self.user)

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
    def test_signup_rate_limit(self):
        # Reseta o rate limit
        cache.clear()
        url = reverse('signup')
        # Tentar fazer vários cadastros (sucesso)
        signupLimitPerHour = config("SIGNUP_LIMIT_PER_HOUR", cast=int)
        for i in range(signupLimitPerHour):
            data = {
                'username': f'user{i}',
                'email': f'user{i}@example.com',
                'password': 'password123'
            }
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Tentativa de cadastro excedendo o limite (deve retornar 429)
        data = {
            'username': 'userLimitExceeded',
            'email': 'userLimitExceeded@example.com',
            'password': 'password123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class LoginRateLimitTest(APITestCase):

    def setUp(self):
        self.username = 'user'
        self.password = 'password123'
        User.objects.create_user(username=self.username, password=self.password)

        self.url = reverse('token_obtain_pair')

    def test_login_rate_limit(self):
        # Reseta o rate limit
        cache.clear()
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
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.force_authenticate(user=self.user)

    def test_get_me_info(self):
        """
        Testa se o endpoint /me retorna as informações do usuário autenticado.
        """
        url = reverse('me')  # ajusta se o nome da rota for diferente
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.username)


from unittest.mock import patch
from users.tasks import send_new_follower_email
from django.test import TestCase

class SendFollowerEmailTest(TestCase):
    @patch('users.tasks.send_mail')
    def test_send_new_follower_email_task(self, mock_send_mail):
        """
        Testa se a task send_new_follower_email chama o send_mail com os argumentos corretos.
        """
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

from posts.models import Post


class ProfileViewTest(APITestCase):
    def setUp(self):
        cache.clear()
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.number_of_followers = 5
        self.number_of_following = 3
        for i in range(self.number_of_followers):
            follower = User.objects.create_user(username=f"follower{i}", password="testpass")
            Follow.objects.create(user=follower, followed_user=self.user)
            if(i < self.number_of_following):
                Follow.objects.create(user=self.user, followed_user=follower)
        self.client.force_authenticate(user=self.user)

    def test_get_profile_by_id(self):
        """
        Testa se o endpoint /users/profile/{user_id} retorna as informações do usuário.
        """
        url = reverse('user-profile', kwargs={'user_id': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["followers_count"], self.number_of_followers)
        self.assertEqual(response.data["following_count"], self.number_of_following)
        self.assertEqual(response.data["username"], self.user.username)

    def test_get_invalid_profile(self):
        """
        Testa se o endpoint /users/profile/{user_id} retorna um erro 404 se o usuário não existir."""
        url = reverse('user-profile', kwargs={'user_id': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_my_profile(self):
        """
        Testa se o endpoint /users/profile retorna as informações do usuário autenticado.
        """
        url = reverse('my-profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user.username)


class UserPostsViewTest(APITestCase):
    def setUp(self):
        cache.clear()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.other_user = User.objects.create_user(username="otheruser", password="testpass")
        Post.objects.create(user=self.user, text="Hello World")
        Post.objects.create(user=self.other_user, text="Goodbye World")
        self.client.force_authenticate(user=self.user)

    def test_get_user_posts(self):
        """
        Testa se o endpoint /users/{user_id}/posts retorna os posts do usuário.
        """
        url = reverse('user-posts', kwargs={'user_id': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["text"], "Hello World")

        url = reverse('user-posts', kwargs={'user_id': self.other_user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["text"], "Goodbye World")

    def test_get_invalid_user_posts(self):
        """
        Testa se o endpoint /users/{user_id}/posts retorna um erro 404 se o usuário nao existir.
        """
        url = reverse('user-posts', kwargs={'user_id': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UserPostsPaginationTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_authenticate(user=self.user)

        # Cria 15 posts para testar paginação
        for i in range(15):
            Post.objects.create(user=self.user, text=f"Post número {i}")

    def test_paginated_user_posts(self):
        url = reverse('user-posts', kwargs={'user_id': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertLessEqual(len(response.data["results"]), 10)  # Página padrão com 10 itens
        self.assertIn("next", response.data)

    def test_second_page_user_posts(self):
        url = reverse('user-posts', kwargs={'user_id': self.user.id}) + "?page=2"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertGreater(len(response.data["results"]), 0)

class SuggestionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="main", password="123456")
        self.client.force_authenticate(user=self.user)

        # Cria alguns usuários
        self.other_users = [
            User.objects.create_user(username=f"user{i}", password="123456")
            for i in range(5)
        ]

        # main segue os 2 primeiros
        Follow.objects.create(user=self.user, followed_user=self.other_users[0])
        Follow.objects.create(user=self.user, followed_user=self.other_users[1])
    def test_suggestions_does_not_include_self_or_followed(self):
        response = self.client.get(reverse("suggestions"))
        self.assertEqual(response.status_code, 200)

        usernames = [u["username"] for u in response.data]

        # Usuários seguidos não devem estar na resposta
        self.assertNotIn("user0", usernames)
        self.assertNotIn("user1", usernames)

        # O próprio usuário não deve estar na resposta
        self.assertNotIn("main", usernames)

        # Os demais devem aparecer
        self.assertIn("user2", usernames)
        self.assertIn("user3", usernames)
        self.assertIn("user4", usernames)

