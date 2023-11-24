from rest_framework import serializers
from .models import Profile, FollowRequest


class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")    
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")
    profile_photo = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    is_follower = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'gender',
            'about_me',
            'is_private',
            'followers',
            'following',
            'is_follower',
            'profile_photo',
        ]

    def get_profile_photo(self, obj):
        return obj.profile_photo.url

    def get_followers(self, obj):
        return obj.followers.count()
    
    def get_following(self, obj):
        return obj.following.count()
    
    def get_is_follower(self, obj):
        current_user_profile = self.context['request'].user.profile
        return obj.check_follower(current_user_profile)

class UpdateProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = [
            'gender',
            'about_me',
            'profile_photo',
            'is_private',
        ]

class FollowSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")    
    last_name = serializers.CharField(source="user.last_name")

    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'about_me',
            'profile_photo',
            'is_private',
        ]

class FollowRequestSerializer(serializers.ModelSerializer):
    requester = ProfileSerializer()
    
    class Meta:
        model = FollowRequest
        fields = [
            "id",
            "updated_at",
            "created_at",
            "accepted",
            "requester",
            "target"
        ]