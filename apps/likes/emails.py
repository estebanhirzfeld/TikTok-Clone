from django.conf import settings
from django.core.mail import send_mail


def send_video_like_notification(sender_user, recipient_user):
    subject = "A user liked your video"
    message = f"Hi there, {recipient_user.first_name}!!, the user {sender_user.first_name} {sender_user.last_name} liked your video"
    from_email = settings.DEFAULT_NO_REPLY_EMAIL
    recipient_list = [recipient_user.email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=True)


def send_comment_like_notification(sender_user, recipient_user, video):
    video_owner = f"{video.user.first_name}'s video"
    if video.user == recipient_user:
        video_owner = "your video"

    subject = "A user liked your comment"
    message = f"Hi there, {recipient_user.first_name}!!, the user {sender_user.first_name} {sender_user.last_name} liked your comment on {video_owner}"
    from_email = settings.DEFAULT_NO_REPLY_EMAIL
    recipient_list = [recipient_user.email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=True)
