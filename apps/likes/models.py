from django.db import models
from apps.common.models import TimeStampedModel
from apps.videos.models import Video
from apps.comments.models import Comment
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

# Create your models here.

class VideoLike(TimeStampedModel):
    user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE)
    video = models.ForeignKey(Video, verbose_name=_("video"), on_delete=models.CASCADE)

    class Meta:
        unique_together = ["user", "video"]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.first_name} liked {self.video.user.first_name}'s video"

class CommentLike(TimeStampedModel):
    user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, verbose_name=_("comment"), on_delete=models.CASCADE)

    class Meta:
        unique_together = ["user", "comment"]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.first_name} liked {self.comment.user.first_name}'s comment"