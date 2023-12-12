from django.urls import path

from .views import (
    LikeCommentCreateDestroyAPIView,
    LikeVideoCreateDestroyAPIView,
    MyLikedCommentsListView,
    MyLikedVideosListView,
    UserLikedVideosListView,
)

urlpatterns = [
    path("videos/", MyLikedVideosListView.as_view(), name="my-liked-videos"),
    path(
        "videos/user/<uuid:id>/",
        UserLikedVideosListView.as_view(),
        name="user-liked-videos",
    ),
    path(
        "video/<uuid:video_id>/",
        LikeVideoCreateDestroyAPIView.as_view(),
        name="add-remove-video-like",
    ),
    path("comments/", MyLikedCommentsListView.as_view(), name="my-liked-comments"),
    path(
        "comment/<uuid:comment_id>/",
        LikeCommentCreateDestroyAPIView.as_view(),
        name="add-remove-comment-like",
    ),
]
