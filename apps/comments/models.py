from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import TimeStampedModel
from apps.videos.models import Video

User = get_user_model()


# Create your models here.
class Comment(TimeStampedModel):
    user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE)
    video = models.ForeignKey(Video, verbose_name=_("video"), on_delete=models.CASCADE)
    content = models.TextField(verbose_name=_("response content"), max_length=300)

    parent_response = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ["created_at"]

    @property
    def reply_count(self):
        return Comment.objects.filter(parent_response=self).count()

    def __str__(self):
        return (
            f"{self.user.first_name} commented on {self.video.user.first_name}'s video"
        )
