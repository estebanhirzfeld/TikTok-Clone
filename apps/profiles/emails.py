from django.core.mail import send_mail
from django.conf import settings

def send_profile_following_notification(sender_profile, recipient_profile):
    subject = "A new user follows you"
    message = f"Hi there, {recipient_profile.user.first_name}!!, the user {sender_profile.user.first_name} {sender_profile.user.last_name} now follows you"
    from_email = settings.DEFAULT_NO_REPLY_EMAIL
    recipient_list = [recipient_profile.user.email]
    
    send_mail(subject, message, from_email, recipient_list, fail_silently=True)

def send_profile_follow_request_notification(sender_profile, recipient_profile):
    subject = "New Follow Request"
    message = f"Hi {recipient_profile.user.first_name}!,\n\n"\
            f"The user {sender_profile.user.first_name} {sender_profile.user.last_name} has sent you a follow request.\n\n"
    from_email = settings.DEFAULT_NO_REPLY_EMAIL
    recipient_list = [recipient_profile.user.email]
    
    send_mail(subject, message, from_email, recipient_list, fail_silently=True)

def send_follow_request_accepted_notification(sender_profile, recipient_profile):
    subject = "Follow Request Accepted"
    message = f"Hi {sender_profile.user.first_name}!,\n\n"\
            f"Great news! {recipient_profile.user.first_name} {recipient_profile.user.last_name} has accepted your follow request.\n\n"\
            f"Now you are following {recipient_profile.user.first_name} {recipient_profile.user.last_name}.\n\n"
    from_email = settings.DEFAULT_NO_REPLY_EMAIL
    recipient_list = [sender_profile.user.email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=True)