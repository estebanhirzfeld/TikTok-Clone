import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from core.settings.base import AUTH_USER_MODEL

from .emails import send_follow_request_accepted_notification
from .models import FollowRequest, Profile

logger = logging.getLogger(__name__)


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        logger.info(f"{instance}'s profile has been created")


@receiver(post_save, sender=FollowRequest)
def follow_on_request_accept(sender, instance, **kwargs):
    if instance.accepted:
        instance.requester.following.add(instance.target)
        instance.target.followers.add(instance.requester)
        logger.info(f"{instance.requester}' is now following --> {instance.target}")

        # Delete the FollowRequest after processing the signal
        instance.delete()


@receiver(post_save, sender=Profile)
def accept_pending_follow_requests(sender, instance, **kwargs):
    if not instance.is_private:  # Check if the profile is now public
        pending_requests = FollowRequest.objects.filter(target=instance, accepted=False)

        for request in pending_requests:
            request.accepted = True
            request.save()

            send_follow_request_accepted_notification(request.requester, request.target)
