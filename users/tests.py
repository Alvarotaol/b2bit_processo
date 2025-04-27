from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from users.models import Follow
from django.urls import reverse

class FollowUserTestCase(APITestCase):
    def setUp(self):
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