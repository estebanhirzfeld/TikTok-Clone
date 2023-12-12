from django.conf import settings
from django.core.mail import send_mail


def send_video_comment_notification(sender_user, recipient_user):
    subject = "A user commented your video"
    message = f"Hi there, {recipient_user.first_name}!!, the user {sender_user.first_name} {sender_user.last_name} commented your video"
    from_email = settings.DEFAULT_NO_REPLY_EMAIL
    recipient_list = [recipient_user.email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=True)


def send_comment_reply_notification(sender_user, recipient_user, video):
    video_owner = f"{video.user.first_name}'s video"
    if video.user == recipient_user:
        video_owner = "your video"

    subject = "A user replied your comment"
    message = f"Hi there, {recipient_user.first_name}!!, the user {sender_user.first_name} {sender_user.last_name} replied your comment on {video_owner}"
    from_email = settings.DEFAULT_NO_REPLY_EMAIL
    recipient_list = [recipient_user.email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=True)
