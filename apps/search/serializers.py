from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from rest_framework import serializers

from .documents import VideoDocument


class VideoElasticSearchSerializer(DocumentSerializer):
    video_id = serializers.UUIDField()
    tags = serializers.ListField(child=serializers.CharField())

    class Meta:
        document = VideoDocument
        fields = [
            "video_id",
            "thumbnail",
            "user_first_name",
            "user_last_name",
            "created_at",
            "tags",
        ]
