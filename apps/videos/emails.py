from django.conf import settings
from django.core.mail import send_mail


def send_video_creation_notification(video_creator, followers):
    subject = "New Video Created by {}".format(video_creator.user.first_name)
    message = "Check out the latest video created by {}.".format(
        video_creator.user.first_name
    )
    from_email = settings.DEFAULT_NO_REPLY_EMAIL
    recipient_list = [follower.user.email for follower in followers]

    send_mail(subject, message, from_email, recipient_list, fail_silently=True)
