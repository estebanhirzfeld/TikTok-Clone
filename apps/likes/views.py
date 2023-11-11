from django.shortcuts import get_object_or_404

from django.http import Http404
from rest_framework import generics, permissions, status, serializers
from rest_framework.response import Response
from .models import VideoLike, CommentLike
from .exceptions import VideoLikeException, VideoLikeAlreadyExistsException, VideoLikeNotFoundException, CommentLikeAlreadyExistsException, CommentLikeException, CommentLikeNotFoundException
from .serializers import VideoLikeSerializer, CommentLikeSerializer
from .emails import send_video_like_notification, send_comment_like_notification

from apps.videos.models import Video
from apps.videos.renderers import VideosJSONRenderer
from apps.videos.serializers import VideoSerializer
from apps.videos.pagination import VideoPagination

from apps.comments.models import Comment
from apps.comments.renderers import CommentsJSONRenderer
from apps.comments.serializers import CommentSerializer
from apps.comments.pagination import CommentPagination

from django.contrib.auth import get_user_model

User = get_user_model()

import logging

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


class LikeVideoCreateDestroyAPIView(generics.CreateAPIView, generics.DestroyAPIView):
    serializer_class = VideoLikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        video_id = kwargs.get('video_id')  
        user = self.request.user
        video = get_object_or_404(Video, id=video_id)

        # Check if the user already liked the video
        if VideoLike.objects.filter(user=user, video=video).exists():
            raise VideoLikeAlreadyExistsException()

        # Create the like
        try:
            serializer = self.get_serializer(data={'user': user.pk, 'video': video.pk})
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user)

            # Notify Liked video by email
            if request.user != video.user:
                send_video_like_notification(request.user, video.user)

            return Response({'detail': 'Video liked successfully.'}, status=status.HTTP_201_CREATED)

        except serializers.ValidationError:
            raise VideoLikeException()

    def delete(self, request, *args, **kwargs):
        video_id = kwargs.get('video_id')  
        video = get_object_or_404(Video, id=video_id)

        # Check if the user has liked the video and delete the like
        video_like = VideoLike.objects.filter(user=request.user, video=video).first()
        if video_like:
            video_like.delete()
            return Response({'detail': 'Video like removed successfully.'}, status=status.HTTP_204_NO_CONTENT)

        # If the user hasn't liked the video, raise a VideoLikeNotFoundException exception
        raise VideoLikeNotFoundException()


class MyLikedCommentsListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CommentPagination
    ordering_fields = [
        "created_at",
        "updated_at",
    ]
    renderer_classes = [CommentsJSONRenderer]

    def get_queryset(self):
        comment_likes = CommentLike.objects.filter(user=self.request.user)
        liked_comments = [like.comment for like in comment_likes]
        return liked_comments


class LikeCommentCreateDestroyAPIView(generics.CreateAPIView, generics.DestroyAPIView):
    serializer_class = CommentLikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        comment_id = kwargs.get('comment_id')  
        user = self.request.user
        comment = get_object_or_404(Comment, id=comment_id)

        # Check if the user already liked the comment
        if CommentLike.objects.filter(user=user, comment=comment).exists():
            raise CommentLikeAlreadyExistsException()

        # Create the like
        try:
            serializer = self.get_serializer(data={'user': user.pk, 'comment': comment.pk})
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user)
            
            # Notify Liked video by email
            if request.user != comment.user:
                send_comment_like_notification(request.user, comment.user, comment.video)

            return Response({'detail': 'Comment liked successfully.'}, status=status.HTTP_201_CREATED)

        except serializers.ValidationError:
            raise CommentLikeException()
        
    def delete(self, request, *args, **kwargs):
        comment_id = kwargs.get('comment_id')  
        comment = get_object_or_404(Comment, id=comment_id)

        # Check if the user has liked the comment and delete the like
        comment_like = CommentLike.objects.filter(user=request.user, comment=comment).first()
        if comment_like:
            comment_like.delete()
            return Response({'detail': 'Comment like removed successfully.'}, status=status.HTTP_204_NO_CONTENT)

        # If the user hasn't liked the comment, raise a CommentLikeNotFoundException exception
        raise CommentLikeNotFoundException()
