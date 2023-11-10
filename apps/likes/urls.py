from django.urls import path
from .views import (
    MyLikedVideosListView,
    UserLikedVideosListView,
    LikeVideoCreateDestroyView,
)

urlpatterns = [
    path("videos/",MyLikedVideosListView.as_view() ,name="my-liked-videos"),
    path("videos/user/<uuid:id>/",UserLikedVideosListView.as_view() ,name="user-liked-videos"),
    path("video/<uuid:video_id>/",LikeVideoCreateDestroyView.as_view() ,name="add-remove-video-like"),

]
