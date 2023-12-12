from django.contrib import admin

from . import models


# Register your models here.
class VideoAdmin(admin.ModelAdmin):
    list_display = ["pkid", "user", "view_count", "video", "thumbnail", "tag_list"]
    list_display_links = ["pkid", "user"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["description", "tags"]
    ordering = ["-created_at"]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("tags")

    def tag_list(self, obj):
        return ", ".join(o.name for o in obj.tags.all())


class VideoViewAdmin(admin.ModelAdmin):
    list_display = ["pkid", "video", "user", "viewer_ip"]
    list_display_links = ["pkid", "video"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["video", "user", "viewer_ip"]


admin.site.register(models.Video, VideoAdmin)
admin.site.register(models.VideoView, VideoViewAdmin)
