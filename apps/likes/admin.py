from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import CommentLike, VideoLike


class VideoLikeAdmin(admin.ModelAdmin):
    list_display = ["user", "video_link", "created_at"]

    search_fields = ["user__first_name", "video__description"]
    list_filter = ["created_at"]

    def video_link(self, obj):
        video_change_url = reverse("admin:videos_video_change", args=[obj.video.pkid])
        return format_html('<a href="{}">{}</a>', video_change_url, obj.video)

    video_link.short_description = "Video"
    list_display_links = ["user", "video_link"]


class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ["user", "comment_link", "created_at"]

    search_fields = ["user__first_name", "comment__description"]
    list_filter = ["created_at"]

    def comment_link(self, obj):
        comment_change_url = reverse(
            "admin:comments_comment_change", args=[obj.comment.pkid]
        )
        return format_html('<a href="{}">{}</a>', comment_change_url, obj.video)

    comment_link.short_description = "Comment"
    list_display_links = ["user", "comment_link"]


admin.site.register(VideoLike, VideoLikeAdmin)
admin.site.register(CommentLike, CommentLikeAdmin)
