from django.urls import path

from .views import (
    FollowingUserVideoListView,
    MyVideoListView,
    UserVideosListView,
    VideoCreateView,
    VideoListView,
    VideoRetrieveUpdateDestroyView,
)

urlpatterns = [
    path("", VideoListView.as_view(), name="video-list"),
    path("me/", MyVideoListView.as_view(), name="my-video-list"),
    path("upload/", VideoCreateView.as_view(), name="video-upload"),
    path(
        "following/", FollowingUserVideoListView.as_view(), name="following-user-videos"
    ),
    path("user/<uuid:id>/", UserVideosListView.as_view(), name="user-videos"),
    path(
        "<uuid:id>/",
        VideoRetrieveUpdateDestroyView.as_view(),
        name="video-retrieve-update-destroy",
    ),
]
