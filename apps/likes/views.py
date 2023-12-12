from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, serializers, status
from rest_framework.response import Response

from apps.comments.models import Comment
from apps.comments.pagination import CommentPagination
from apps.comments.renderers import CommentsJSONRenderer
from apps.comments.serializers import CommentSerializer
from apps.videos.models import Video
from apps.videos.pagination import VideoPagination
from apps.videos.renderers import VideosJSONRenderer
from apps.videos.serializers import VideoSerializer

from .emails import (
    send_comment_like_notification,
    send_video_like_notification,
)
from .exceptions import (
    CommentLikeAlreadyExistsException,
    CommentLikeException,
    CommentLikeNotFoundException,
    VideoLikeAlreadyExistsException,
    VideoLikeException,
    VideoLikeNotFoundException,
)
from .models import CommentLike, VideoLike
from .serializers import CommentLikeSerializer, VideoLikeSerializer

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
        liked_video_ids = [like.video.id for like in video_likes]

        queryset = Video.objects.filter(
            Q(user__profile__is_private=False)
            | Q(  # Videos where user profile is not private
                user__profile__followers=self.request.user.profile
            )
            | Q(  # Videos where user is followed by request user
                user=self.request.user
            ),  # Videos where user is the request user
            id__in=liked_video_ids,  # Only include videos that are liked by the specified user
        )

        return queryset


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

        # Get liked videos by the specified user
        video_likes = VideoLike.objects.filter(user=user)
        liked_video_ids = [like.video.id for like in video_likes]

        queryset = Video.objects.filter(
            Q(user__profile__is_private=False)
            | Q(  # Videos where user profile is not private
                user__profile__followers=self.request.user.profile
            )
            | Q(  # Videos where user is followed by request user
                user=self.request.user
            ),  # Videos where user is the request user
            id__in=liked_video_ids,  # Only include videos that are liked by the specified user
        )

        return queryset


class LikeVideoCreateDestroyAPIView(generics.CreateAPIView, generics.DestroyAPIView):
    serializer_class = VideoLikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        video_id = kwargs.get("video_id")
        user = self.request.user
        video = get_object_or_404(Video, id=video_id)

        # Check if the video's user is private
        if video.user.profile.is_private:
            # Check if the user is not the video owner
            if user != video.user:
                # Check if the requesting user is following the video's user
                if not user.profile.check_following(video.user.profile):
                    return Response(
                        {
                            "detail": "You cannot like this video because the user is private and you are not following them."
                        },
                        status=status.HTTP_403_FORBIDDEN,
                    )

        # Check if the user already liked the video
        if VideoLike.objects.filter(user=user, video=video).exists():
            raise VideoLikeAlreadyExistsException()

        # Create the like
        try:
            serializer = self.get_serializer(data={"user": user.pk, "video": video.pk})
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user)

            # Notify Liked video by email
            if request.user != video.user:
                send_video_like_notification(request.user, video.user)

            return Response(
                {"detail": "Video liked successfully."}, status=status.HTTP_201_CREATED
            )

        except serializers.ValidationError:
            raise VideoLikeException()

    def delete(self, request, *args, **kwargs):
        video_id = kwargs.get("video_id")
        video = get_object_or_404(Video, id=video_id)

        # Check if the video's user is private
        if video.user.profile.is_private:
            # Check if the user is not the video owner
            if request.user != video.user:
                # Check if the requesting user is following the video's user
                if not request.user.profile.check_following(video.user.profile):
                    return Response(
                        {
                            "detail": "You cannot remove the like from this video because the user is private and you are not following them."
                        },
                        status=status.HTTP_403_FORBIDDEN,
                    )

        # Check if the user has liked the video and delete the like
        video_like = VideoLike.objects.filter(user=request.user, video=video).first()
        if video_like:
            video_like.delete()
            return Response(
                {"detail": "Video like removed successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )

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
        liked_comment_ids = [like.comment.id for like in comment_likes]

        queryset = Comment.objects.filter(
            Q(user__profile__is_private=False)
            | Q(  # Comments on posts where the user profile is not private
                user__profile__followers=self.request.user.profile
            )
            | Q(  # Comments on posts where the user is followed by the request user
                user=self.request.user
            ),  # Comments on posts where the user is the request user
            id__in=liked_comment_ids,  # Only include comments that are liked by the authenticated user
        )

        return queryset


class LikeCommentCreateDestroyAPIView(generics.CreateAPIView, generics.DestroyAPIView):
    serializer_class = CommentLikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        comment_id = kwargs.get("comment_id")
        user = self.request.user
        comment = get_object_or_404(Comment, id=comment_id)

        # Check if the user already liked the comment
        if CommentLike.objects.filter(user=user, comment=comment).exists():
            raise CommentLikeAlreadyExistsException()

        # Create the like
        try:
            serializer = self.get_serializer(
                data={"user": user.pk, "comment": comment.pk}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user)

            # Notify Liked video by email
            if request.user != comment.user:
                send_comment_like_notification(
                    request.user, comment.user, comment.video
                )

            return Response(
                {"detail": "Comment liked successfully."},
                status=status.HTTP_201_CREATED,
            )

        except serializers.ValidationError:
            raise CommentLikeException()

    def delete(self, request, *args, **kwargs):
        comment_id = kwargs.get("comment_id")
        comment = get_object_or_404(Comment, id=comment_id)

        # Check if the user has liked the comment and delete the like
        comment_like = CommentLike.objects.filter(
            user=request.user, comment=comment
        ).first()
        if comment_like:
            comment_like.delete()
            return Response(
                {"detail": "Comment like removed successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )

        # If the user hasn't liked the comment, raise a CommentLikeNotFoundException exception
        raise CommentLikeNotFoundException()
