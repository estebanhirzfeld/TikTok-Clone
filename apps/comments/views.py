from django.shortcuts import render
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
        return Comment.objects.filter(video=video, parent_response=None)

    def perform_create(self, serializer):
        user = self.request.user
        video_id = self.kwargs.get("video_id")
        video = get_object_or_404(Video, id=video_id)
        serializer.save(user=user, video=video)
        send_video_comment_notification(user, video.user)

class CommentRepliesListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated]
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
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly] 
    lookup_field = 'comment_id'

    def get_object(self):
        comment_id = self.kwargs.get(self.lookup_field)
        return get_object_or_404(Comment, id=comment_id)

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        self.perform_destroy(comment)
        return Response(status=status.HTTP_204_NO_CONTENT)