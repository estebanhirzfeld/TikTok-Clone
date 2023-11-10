from django.urls import reverse
from django.utils.html import format_html
from django.contrib import admin
from .models import VideoLike

class VideoLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'video_link', 'created_at']

    search_fields = ['user__first_name', 'video__description']
    list_filter = ['created_at']

    def video_link(self, obj):
        video_change_url = reverse('admin:videos_video_change', args=[obj.video.pkid])
        return format_html('<a href="{}">{}</a>', video_change_url, obj.video)
    
    video_link.short_description = 'Video'
    list_display_links = ['user', 'video_link']

admin.site.register(VideoLike, VideoLikeAdmin)
