from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post
from users.models import Follow
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient



class PostModelTest(TestCase):
    def setUp(self):
        # Cria um usuário para associar ao post
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_post_creation(self):
        # Cria um post
        post = Post.objects.create(user=self.user, text="Test Post")

        # Verifica se o post foi salvo corretamente
        self.assertEqual(post.text, "Test Post")
        self.assertEqual(post.user.username, 'testuser')
        self.assertIsNotNone(post.created_at)  # Verifica se a data foi definida

class PostViewTest(TestCase):
    def setUp(self):
        # Cria um usuário para os testes
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)  # Autentica o cliente como o usuário

    def test_create_post(self):
        # Verifica se a criação de post funciona corretamente
        url = reverse('post-list-create')
        data = {'text': 'Test Post', 'image': None}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().text, 'Test Post')

    def test_list_posts(self):
        # Verifica se a listagem de posts funciona corretamente
        Post.objects.create(user=self.user, text='Post 1')
        Post.objects.create(user=self.user, text='Post 2')

        url = reverse('post-list-create')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_create_post_without_authentication(self):
        # Verifica que um usuário não autenticado não pode criar posts
        self.client.logout()  # Desloga o cliente
        url = reverse('post-list-create')
        data = {'text': 'Test Post', 'image': None}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_post(self):
        # Teste de atualização de post
        post = Post.objects.create(user=self.user, text='Original Post')
        url = reverse('post-detail', kwargs={'pk': post.id})
        data = {'text': 'Updated Post'}
        response = self.client.put(url, data, format='json')

        post.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(post.text, 'Updated Post')

    def test_delete_post(self):
        # Teste de deleção de post
        post = Post.objects.create(user=self.user, text='Post to delete')
        url = reverse('post-detail', kwargs={'pk': post.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)

    def test_like_post(self):
        # Teste de like de post
        post = Post.objects.create(user=self.user, text='Post to like')
        url = reverse('like-post', kwargs={'post_id': post.id})

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(post.post_likes.count(), 1)

        # Teste de deslike de post
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(post.post_likes.count(), 0)

    # Teste de like de post inexistente
    def test_like_nonexistent_post(self):
        url = reverse('like-post', kwargs={'post_id': 999})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class FeedTests(TestCase):
    def setUp(self):
        # Cria um usuário para os testes
        self.user = User.objects.create_user(username='user1', password='pass')
        self.other_user = User.objects.create_user(username='user2', password='pass')

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)  # Autentica o cliente como o usuário

    def test_feed_returns_followed_users_posts(self):
        Follow.objects.create(user=self.user, followed_user=self.other_user)

        post = Post.objects.create(user=self.other_user, text='Post by followed user')

        response = self.client.get('/api/feed/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["text"], 'Post by followed user')