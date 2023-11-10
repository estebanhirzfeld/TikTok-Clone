from django.shortcuts import get_object_or_404

from django.http import Http404
from rest_framework import generics, permissions, status, serializers
from rest_framework.response import Response
from .models import VideoLike
from .exceptions import VideoLikeException, VideoLikeAlreadyExistsException, VideoLikeNotFoundException
from .serializers import VideoLikeSerializer
from .emails import send_video_like_notification

from apps.videos.models import Video
from apps.videos.renderers import VideosJSONRenderer
from apps.videos.serializers import VideoSerializer
from apps.videos.pagination import VideoPagination
from apps.videos.exceptions import VideoNotFoundException


from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.
class MyLikedVideosListView(generics.ListAPIView):
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = VideoPagination
    ordering_fields = [
        "created_at",
        "updated_at",
    ]
    renderer_classes = [VideosJSONRenderer]

    def get_queryset(self):
        video_likes = VideoLike.objects.filter(user=self.request.user)
        liked_videos = [like.video for like in video_likes]
        return liked_videos


class UserLikedVideosListView(generics.ListAPIView):
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = VideoPagination
    ordering_fields = [
        "created_at",
        "updated_at",
    ]
    renderer_classes = [VideosJSONRenderer]

    def get_queryset(self):
        user_id = self.kwargs.get("id")
        user = User.objects.get(id=user_id)
        video_likes = VideoLike.objects.filter(user=user)
        liked_videos = [like.video for like in video_likes]
        return liked_videos


class LikeVideoCreateDestroyView(generics.CreateAPIView, generics.DestroyAPIView):
    serializer_class = VideoLikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_video_or_404(self, video_id):
        try:
            video = get_object_or_404(Video, id=video_id)
            return video
        except:
            raise VideoNotFoundException()

    def perform_like(self, video):
        # Check if the user already liked the video
        if VideoLike.objects.filter(user=self.request.user, video=video).exists():
            raise VideoLikeAlreadyExistsException()

        try:
            serializer = self.get_serializer(data={'user': self.request.user.pk, 'video': video.pk})
            serializer.is_valid(raise_exception=True)
            serializer.save(user=self.request.user)

        except serializers.ValidationError as e:
            raise VideoLikeException()

    def post(self, request, *args, **kwargs):
        video_id = kwargs.get('video_id')  
        video = self.get_video_or_404(video_id)
        self.perform_like(video)

        # Notify Liked video by email
        if request.user != video.user:
            send_video_like_notification(request.user, video.user)

        return Response({'detail': 'Video liked successfully.'}, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        video_id = kwargs.get('video_id')  
        video = self.get_video_or_404(video_id)

        # Check if the user has liked the video and delete the like
        video_like = VideoLike.objects.filter(user=request.user, video=video).first()
        if video_like:
            video_like.delete()
            return Response({'detail': 'Video like removed successfully.'}, status=status.HTTP_204_NO_CONTENT)

        # If the user hasn't liked the video, raise a VideoLikeNotFoundException exception
        raise VideoLikeNotFoundException()
