from django.core.mail import send_mail
from django.conf import settings

def send_profile_following_notification(sender_profile, recipient_profile):
    subject = "A new user follows you"
    message = f"Hi there, {recipient_profile.user.first_name}!!, the user {sender_profile.user.first_name} {sender_profile.user.last_name} now follows you"
    from_email = settings.DEFAULT_NO_REPLY_EMAIL
    recipient_list = [recipient_profile.user.email]
    
    send_mail(subject, message, from_email, recipient_list, fail_silently=True)
