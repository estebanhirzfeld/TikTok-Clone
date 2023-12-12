from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django_elasticsearch_dsl.registries import registry

from apps.profiles.models import Profile
from apps.videos.models import Video


@receiver(post_save, sender=Video)
def update_document(sender, instance=None, created=False, **kwargs):
    """Update the VideoDocument in Elasticsearch when a video instance is updated or created"""
    registry.update(instance)


@receiver(post_delete, sender=Video)
def delete_document(sender, instance=None, **kwargs):
    """Delete the VideoDocument in Elasticsearch when a video instance is deleted"""
    registry.delete(instance)


@receiver(post_save, sender=Profile)
def update_related_videos(sender, instance, **kwargs):
    """
    Update related videos in Elasticsearch when the is_private field of the profile changes.
    """
    related_videos = instance.user.videos.all()

    # Update each related video in the Elasticsearch index
    for video in related_videos:
        registry.update(video)
