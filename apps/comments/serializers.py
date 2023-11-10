from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user_first_name = serializers.CharField(source="user.first_name", read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "user_first_name",
            "parent_response",
            "content",
            "replies",
            "created_at",
        ]

    def get_replies(self, obj):
        return obj.reply_count  
