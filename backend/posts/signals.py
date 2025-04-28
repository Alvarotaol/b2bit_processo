from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
from .tasks import invalidate_followers_feed

@receiver(post_save, sender=Post)
def invalidate_feed_cache(sender, instance, created, **kwargs):
    if created:
        invalidate_followers_feed(instance.user.id)

