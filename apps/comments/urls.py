from django.urls import path

from .views import (
    CommentListCreateView,
    CommentRepliesListCreateView,
    CommentDestroyView,
    )

urlpatterns = [
    path("video/<uuid:video_id>/", CommentListCreateView.as_view(), name="video-comments",),
    path('<uuid:comment_id>/replies/', CommentRepliesListCreateView.as_view(), name='comment-replies-list-create'),
    path('<uuid:comment_id>/', CommentDestroyView.as_view(), name='comment-delete'),
]
