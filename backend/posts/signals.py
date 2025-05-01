from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Post, Like
from users.models import Follow
from .tasks import invalidate_followers_feed

@receiver([post_save, post_delete], sender=Post)
@receiver([post_save, post_delete], sender=Like)
@receiver([post_save, post_delete], sender=Follow)
def invalidate_feed_cache(sender, instance, **kwargs):
    invalidate_followers_feed(instance.user.id)
