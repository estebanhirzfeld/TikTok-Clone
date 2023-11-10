from rest_framework import serializers
from .models import VideoLike


class VideoLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoLike
        fields = ['user', 'video']