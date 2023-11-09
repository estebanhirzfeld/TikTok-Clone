from django.urls import path

from .views import (
    VideoListView,
    VideoCreateView,
    VideoRetrieveUpdateDestroyView,
)

urlpatterns = [
    path("", VideoListView.as_view(), name="video-list"),
    path("upload/", VideoCreateView.as_view(), name="video-upload"),
    path("<uuid:id>/",VideoRetrieveUpdateDestroyView.as_view(), name="video-retrieve-update-destroy",),
]