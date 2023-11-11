from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user_first_name = serializers.CharField(source="user.first_name", read_only=True)
    likes = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "user_first_name",
            "parent_response",
            "content",
            "replies",
            "likes",
            "created_at",
        ]

    def get_replies(self, obj):
        return obj.reply_count  
    
    def get_likes(self, obj):
        return obj.commentlike_set.count()