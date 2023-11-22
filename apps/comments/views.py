from django.shortcuts import render
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .permissions import IsOwnerOrReadOnly
from .models import Comment
from .serializers import CommentSerializer
from .pagination import CommentPagination
from .renderers import CommentsJSONRenderer, CommentRepliesJSONRenderer
from rest_framework.generics import get_object_or_404
from apps.videos.models import Video
from .emails import send_video_comment_notification, send_comment_reply_notification

from apps.profiles.permissions import CanAccessPrivateContent
from django.db.models import Q
import logging


# Create your views here.
class MyCommentListView(generics.ListAPIView):
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentSerializer
    pagination_class = CommentPagination
    renderer_classes = [CommentsJSONRenderer]

    def get_queryset(self):
        return Comment.objects.filter(user = self.request.user)

class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentSerializer
    pagination_class = CommentPagination
    renderer_classes = [CommentsJSONRenderer]

    def get_queryset(self):
        video_id = self.kwargs.get("video_id")
        video = get_object_or_404(Video, id=video_id)
        
        queryset = Comment.objects.filter(
            Q(video__user__profile__is_private=False) |                     # Comments where video user profile is not private
            Q(video__user__profile__followers=self.request.user.profile) |  # Comments where video user is followed by request user
            Q(video__user=self.request.user)                                # Comments where video user is the request user
        )
        queryset = queryset.filter(video=video, parent_response=None)
        return queryset


    def perform_create(self, serializer):
        user = self.request.user
        video = get_object_or_404(Video, id=self.kwargs.get("video_id"))
        video_user = video.user.profile

        # Check if the user has permission to comment 
        if not video_user.is_private or video_user.check_follower(user) or video.user == user:

            serializer.save(user=user, video=video, parent_response=None)
            send_video_comment_notification(user, video.user)
        else:
            raise PermissionDenied("You do not have permission to comment on this video.")


class CommentRepliesListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated, CanAccessPrivateContent]
    serializer_class = CommentSerializer
    pagination_class = CommentPagination
    renderer_classes = [CommentRepliesJSONRenderer]

    def get_queryset(self):
        comment_id = self.kwargs.get("comment_id")
        parent_response = get_object_or_404(Comment, id=comment_id)
        return Comment.objects.filter(parent_response=parent_response)

    def perform_create(self, serializer):
        user = self.request.user
        comment_id = self.kwargs.get("comment_id")
        parent_response = get_object_or_404(Comment, id=comment_id)
        serializer.save(user=user, video=parent_response.video, parent_response=parent_response)
        send_comment_reply_notification(user, parent_response.user, parent_response.video)

class CommentDestroyView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly] 
    lookup_field = 'id'
