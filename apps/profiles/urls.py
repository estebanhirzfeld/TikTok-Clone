from django.urls import path

from .views import (
    ProfileListAPIView,

    YourProfileDetailView,
    UpdateProfileAPIView,
    YourFollowersListView,
    YourFollowingListView,

    ProfileDetailAPIView,
    FollowersListView,
    FollowingListView,
    
    FollowAPIView,
    UnfollowAPIView,
)

urlpatterns = [
    path("all/", ProfileListAPIView.as_view(), name="all-profiles"),

    path("me/", YourProfileDetailView.as_view(), name="my-profile"),
    path("me/update/", UpdateProfileAPIView.as_view(), name="update-profile"),
    path("me/followers/", YourFollowersListView.as_view(), name="my-followers"),
    path("me/following/", YourFollowingListView.as_view(), name="my-following"),

    path("<uuid:user_id>/profile/", ProfileDetailAPIView.as_view(), name="user-profile"),
    path("<uuid:user_id>/followers/", FollowersListView.as_view(), name="user-followers"),
    path("<uuid:user_id>/following/", FollowingListView.as_view(), name="user-following"),

    path("<uuid:user_id>/follow/", FollowAPIView.as_view(), name="follow"),
    path("<uuid:user_id>/unfollow/", UnfollowAPIView.as_view(), name="unfollow"),
]