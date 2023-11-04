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

    followers = models.ManyToManyField("self", verbose_name=_("followers"), blank=True, related_name="following", symmetrical=False)

    def __str__(self) -> str:
        return f"{self.user.first_name}'s Profile"
    
    def follow(self, profile):
        self.followers.add(profile)

    def unfollow(self, profile):
        self.followers.remove(profile)

    def check_following(self, profile):
        return self.followers.filter(pkid=profile.pkid).exists()
