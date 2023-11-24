from django.utils.translation import gettext_lazy as _
from django.db import models
from apps.common.models import TimeStampedModel
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Profile(TimeStampedModel):
    class Gender(models.TextChoices):
        MALE = 'M', _("Male")
        FEMALE = 'F', _("Female")
        OTHER = 'O', _("Other")

    user = models.OneToOneField(User, verbose_name=_("user"), on_delete=models.CASCADE, related_name="profile")
    gender = models.CharField(verbose_name=_("gender"), max_length=1, choices=Gender.choices, default=Gender.OTHER)
    about_me = models.CharField(_("about me"), max_length=50)
    profile_photo = models.ImageField(_("profile photo"), default='/profile_placeholder.png')
    is_private = models.BooleanField(_("is profile private"), default=False)

    following = models.ManyToManyField("self", verbose_name=_("following"), blank=True, related_name="followers", symmetrical=False)

    def __str__(self) -> str:
        return f"{self.user.first_name}'s Profile"
    
    def follow(self, profile):
        self.following.add(profile)

    def unfollow(self, profile):
        self.following.remove(profile)

    def check_following(self, profile):
        return self.following.filter(pk=profile.pk).exists()

    def check_follower(self, profile):
        return self.followers.filter(pk=profile.pk).exists()

class FollowRequest(TimeStampedModel):
    requester = models.ForeignKey(Profile, verbose_name=_("requester user"), on_delete=models.CASCADE, related_name='follow_requests_sent')
    target = models.ForeignKey(Profile, verbose_name=_("target user"), on_delete=models.CASCADE, related_name='follow_requests_received')
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ['requester', 'target']

    def __str__(self):
        return f'{self.requester.user.first_name} -> {self.target.user.first_name}'
