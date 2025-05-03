from django.contrib.auth import get_user_model
from .models import Post
import random

User = get_user_model()

def run():
    user, _ = User.objects.get_or_create(username="testuser")
    user.set_password("testpass")
    user.save()

    contents = [
        "Trabalhando no projeto",
        "Corrigindo bug chato",
        "Finalizei a feature de login",
        "Atualizei a documentação",
        "Deploy feito com sucesso!",
        "Mais um dia de código",
        "Aprendi algo novo hoje",
        "Revisando PRs",
        "Criando testes automatizados",
        "Pensando em refatorar isso aqui..."
    ]

    posts = [
        Post(user=user, text=random.choice(contents))
        for _ in range(50)
    ]
    Post.objects.bulk_create(posts)
    print("Seed finalizado com 50 posts.")
