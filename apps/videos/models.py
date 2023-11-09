from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from django.db import models
from apps.common.models import TimeStampedModel
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager

User = get_user_model()


class Video(TimeStampedModel):
    user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE, related_name="videos")
    thumbnail = models.ImageField(verbose_name=_("video thumbnail"), default='/video_thumbnail_placeholder.png')
    video = models.FileField(
        verbose_name=_("video"),
        null=True,
        blank=True,
        default='/video_file_placeholder.png',
        validators=[FileExtensionValidator(allowed_extensions=['mp4','avi','mkv','MOV'])]
    )
    description = models.CharField(verbose_name=_("description"), max_length=255,null=True, blank=True,)
    tags = TaggableManager()

    def __str__(self):
        return f"{self.user.first_name}'s video"
    
    def view_count(self):
        return self.video_views.count()

class VideoView(TimeStampedModel):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="video_views")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="user_views")
    viewer_ip = models.GenericIPAddressField(verbose_name=_("viewer IP"), null=True, blank=True)

    class Meta:
        verbose_name = _("Video View")
        verbose_name_plural = _("Video Views")
        unique_together = ("video", "user", "viewer_ip")

    def __str__(self):
        return f"{self.user.first_name}'s video viewed by {self.user.first_name if self.user else 'Anonymous'} from IP {self.viewer_ip}"

    @classmethod
    def record_view(cls, video, user, viewer_ip):
        view, _ = cls.objects.get_or_create(video=video, user=user, viewer_ip=viewer_ip)
        view.save()
