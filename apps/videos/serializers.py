from rest_framework import serializers
from .models import Video, VideoView
from apps.profiles.serializers import ProfileSerializer
from taggit.models import Tag
import json
from .validators import validate_video_format, validate_video_size, validate_thumbnail_image_format


class TagListField(serializers.Field):
    def to_representation(self, value):
        return [tag.name for tag in value.all()]

    def to_internal_value(self, data):
        if isinstance(data, str):
            try:
                # Attempt to deserialize the string using json.loads()
                tag_list = json.loads(data)
            except json.JSONDecodeError:
                # If deserialization fails, treat the string as a single element list
                tag_list = [data]
        elif isinstance(data, list):
            tag_list = data
        else:
            raise serializers.ValidationError("Expected a list of tags")

        # Process the list of tags as needed
        tag_objects = []
        for tag_name in tag_list:
            tag_name = tag_name.strip()
            if tag_name:
                tag_objects.append(tag_name)

        return tag_objects


class VideoSerializer(serializers.ModelSerializer):
    user_info = ProfileSerializer(source="user.profile", read_only=True)
    video = serializers.FileField(
        validators=[validate_video_format, validate_video_size]
        )
    thumbnail = serializers.ImageField(required=False, validators=[validate_thumbnail_image_format])
    tags = TagListField(required=False)
    views = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    
    def get_views(self, obj):
        return VideoView.objects.filter(video=obj).count()

    def get_thumbnail(self, obj):
        return obj.thumbnail.url
    
    def get_video(self, obj):
        return obj.video.url

    def get_created_at(self, obj):
        now = obj.created_at
        formatted_date = now.strftime("%m/%d/%Y, %H:%M:%S")
        return formatted_date

    def get_updated_at(self, obj):
        then = obj.updated_at
        formatted_date = then.strftime("%m/%d/%Y, %H:%M:%S")
        return formatted_date

    def create(self, validated_data):
        tags = validated_data.pop("tags", [])  
        video = Video.objects.create(**validated_data)

        # Convert the tags to Tag objects
        tag_objects = [Tag.objects.get_or_create(name=tag.strip())[0] for tag in tags]
        video.tags.set(tag_objects)

        return video

    def update(self, instance, validated_data):
        instance.thumbnail = validated_data.get(
            "thumbnail", instance.thumbnail
        )
        instance.updated_at = validated_data.get("updated_at", instance.updated_at)

        if "tags" in validated_data:
            instance.tags.set(validated_data["tags"])

        instance.save()
        return instance
    
    class Meta:
        model = Video
        fields = [
            "id",
            "video",
            "description",
            "user_info",
            "thumbnail",
            "tags",
            "views",
            "created_at",
            "updated_at",
        ]
