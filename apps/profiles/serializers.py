from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")    
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")
    profile_photo = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'gender',
            'about_me',
            'profile_photo',
        ]

    def get_profile_photo(self, obj):
        return obj.profile_photo.url

class UpdateProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = [
            'gender',
            'about_me',
            'profile_photo',
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
        ]
