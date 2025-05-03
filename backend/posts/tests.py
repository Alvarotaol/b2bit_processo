from django.contrib.auth.models import User
from users.models import Follow
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.core.files.images import ImageFile
from django.core.cache import cache
from .models import Post
from PIL import Image
import io
import os

def generate_fake_image(name="test_image.jpg", size=(100, 100), color=(255, 0, 0)):
    """Generates a fake image file for testing."""
    image = Image.new("RGB", size, color)
    temp_io = io.BytesIO()
    image.save(temp_io, "jpeg")
    temp_io.seek(0)
    return ImageFile(temp_io, name=name)

class PostViewTest(APITestCase):
    def setUp(self):
        cache.clear()
        # Cria um usuário para os testes
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_authenticate(user=self.user)  # Autentica o cliente como o usuário

    def test_create_post(self):
        # Verifica se a criação de post funciona corretamente
        url = reverse('post-list-create')
        data = {'text': 'Test Post', 'image': None}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().text, 'Test Post')

    def test_create_and_delete_post_with_image(self):
        """
        Testa a criação de post com imagem.
        """
        url = reverse('post-list-create')
        image = generate_fake_image()
        data = {"text": "Post with image", "image": image}
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        post = Post.objects.filter(id=response.data['id']).first()

        image_path = post.image.path
        self.assertTrue(os.path.exists(image_path))

        url = reverse('post-detail', kwargs={'pk': response.data['id']})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(os.path.exists(image_path))

        if os.path.exists(image_path):
            os.remove(image_path)


    def test_list_posts(self):
        # Verifica se a listagem de posts funciona corretamente
        Post.objects.create(user=self.user, text='Post 1')
        Post.objects.create(user=self.user, text='Post 2')

        url = reverse('post-list-create')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_paginated_list_posts(self):
        Post.objects.bulk_create([
            Post(user=self.user, text=f'Post {i}') for i in range(1, 15)
        ])

        url = reverse('post-list-create')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 14)
        self.assertEqual(len(response.data['results']), 10)

        url += '?page=2'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 14)
        self.assertEqual(len(response.data['results']), 4)

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

    def test_delete_nonexistent_post(self):
        # Teste de deleção de post inexistente
        url = reverse('post-detail', kwargs={'pk': 999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_nonexistent_post(self):
        # Teste de atualização de post inexistente
        url = reverse('post-detail', kwargs={'pk': 999})
        data = {'text': 'Updated Post'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_another_user_post(self):
        # Teste de tentativa de deleção de post de outro usuário
        other_user = User.objects.create_user(username='other_user', password='pass')
        post = Post.objects.create(user=other_user, text='Post to delete')
        url = reverse('post-detail', kwargs={'pk': post.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

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

    def test_like_nonexistent_post(self):
        # Teste de like de post inexistente
        url = reverse('like-post', kwargs={'post_id': 999})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class FeedTests(APITestCase):
    def setUp(self):
        cache.clear()
        # Cria um usuário para os testes
        self.user = User.objects.create_user(username='user1', password='pass')
        self.other_user = User.objects.create_user(username='user2', password='pass')

        self.client.force_authenticate(user=self.user)  # Autentica o cliente como o usuário

    def test_feed_returns_followed_users_posts(self):
        Follow.objects.create(user=self.user, followed_user=self.other_user)

        Post.objects.create(user=self.other_user, text='Post by followed user')

        response = self.client.get('/api/feed/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["text"], 'Post by followed user')

        # Repete para pegar o resultado do cache
        response = self.client.get('/api/feed/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["text"], 'Post by followed user')


class PostSearchTest(APITestCase):
    def setUp(self):
        cache.clear()
        # Cria um usuário para os testes
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_authenticate(user=self.user)

        # Cria alguns posts para testar a pesquisa
        Post.objects.create(user=self.user, text='Post sobre trabalho')
        Post.objects.create(user=self.user, text='Post sobre diversão')
        Post.objects.create(user=self.user, text='Outro post sobre trabalho')

    def test_search_posts_by_keyword(self):
        # Verifica se a pesquisa por palavra-chave retorna os posts corretos
        url = reverse('post-search')
        response = self.client.get(url, {'q': 'trabalho'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertIn('trabalho', response.data['results'][0]['text'])
        self.assertIn('trabalho', response.data['results'][1]['text'])

    def test_search_posts_empty(self):
        # Verifica se a pesquisa sem palavra-chave retorna todos os posts
        url = reverse('post-search')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)

    def test_search_posts_no_results(self):
        # Verifica se a pesquisa por uma palavra que não existe retorna 0 resultados
        url = reverse('post-search')
        response = self.client.get(url, {'q': 'nada'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

class PostImageEditTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass")
        self.client.force_authenticate(user=self.user)
        # Cria um post sem imagem
        self.post = Post.objects.create(user=self.user, text="Original")

        # Cria um post com imagem
        self.image = generate_fake_image("original.png")
        self.post_with_image = Post.objects.create(user=self.user, text="With image", image=self.image)
        #self.generated_images_path = [self.post_with_image.image.path]

    def test_add_image_to_post(self):
        image = generate_fake_image("add.png")
        url = reverse("post-detail", kwargs={"pk": self.post.id})
        response = self.client.put(url, {"text": "Now with image", "image": image}, format="multipart")
        self.assertEqual(response.status_code, 200)
        self.assertIn("image", response.data)
        basePost = Post.objects.get(id=self.post.id)
        self.assertTrue(basePost.image)


    def test_replace_image(self):
        new_image = generate_fake_image("replace.png")
        old_image = Post.objects.get(id=self.post_with_image.id).image

        url = reverse("post-detail", kwargs={"pk": self.post_with_image.id})
        response = self.client.put(url, {"text": "Updated", "image": new_image}, format="multipart")

        self.assertEqual(response.status_code, 200)
        self.assertIn("image", response.data)
        self.assertNotIn(old_image.path, response.data["image"]) #Tem uma chance pequena de falhar mesmo estando certo

        #Assegura que a imagem antiga foi removida do disco
        self.assertFalse(os.path.exists(old_image.path))

    def test_edit_text_only_keep_image(self):
        url = reverse("post-detail", kwargs={"pk": self.post_with_image.id})
        response = self.client.put(url, {"text": "Only text change"}, format="multipart")
        self.assertEqual(response.status_code, 200)
        self.assertIn("image", response.data)
        self.assertIsNotNone(Post.objects.get(id=self.post_with_image.id).image)


    def test_remove_image(self):
        url = reverse("post-detail", kwargs={"pk": self.post_with_image.id})
        response = self.client.put(url, {"text": "Removed image", "image": ""}, format="multipart")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.get(id=self.post_with_image.id).image, "")

    def tearDown(self):
        for post in Post.objects.all():
            if post.image:
                os.remove(post.image.path)