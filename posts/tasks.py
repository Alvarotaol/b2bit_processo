# posts/tasks.py
from celery import shared_task
from django.core.cache import cache
from users.models import Follow

@shared_task
def invalidate_followers_feed(user_id):

    followers = Follow.objects.filter(followed_user_id=user_id)
    print("deletando cache")
    for follower in followers:
        cache.delete(f"feed_{follower.user_id}")
    cache.delete(f"feed_{user_id}")
