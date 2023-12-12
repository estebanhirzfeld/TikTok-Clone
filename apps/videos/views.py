import logging

from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
from django.db.models import Q
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from apps.profiles.models import Profile
from apps.profiles.permissions import CanAccessPrivateContent

from .emails import send_video_creation_notification
from .exceptions import VideoNotFoundException
from .filters import VideoFilter
from .models import Video, VideoView
from .pagination import VideoPagination
from .permissions import IsOwnerOrReadOnly
from .renderers import VideoJSONRenderer, VideosJSONRenderer
from .serializers import VideoSerializer

# Create your views here.

logger = logging.getLogger(__name__)

User = get_user_model()


class VideoListView(generics.ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = VideoPagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = VideoFilter
    ordering_fields = [
        "created_at",
        "updated_at",
    ]
    renderer_classes = [VideosJSONRenderer]

    def get_queryset(self):
        queryset = Video.objects.filter(
            Q(user__profile__is_private=False)
            | Q(  # Videos where user profile is not private
                user__profile__followers=self.request.user.profile
            )
            | Q(  # Videos where user is followed by request user
                user=self.request.user
            )  # Videos where user is the request user
        )
        return queryset


class MyVideoListView(generics.ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = VideoPagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = VideoFilter
    ordering_fields = [
        "created_at",
        "updated_at",
    ]
    renderer_classes = [VideosJSONRenderer]

    def get_queryset(self):
        return Video.objects.filter(user=self.request.user)


class FollowingUserVideoListView(generics.ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = VideoPagination
    ordering_fields = [
        "created_at",
        "updated_at",
    ]
    renderer_classes = [VideosJSONRenderer]

    def get_queryset(self):
        queryset = self.queryset

        following_users = self.request.user.profile.following.values("user")
        queryset = queryset.filter(user__in=following_users)
        return queryset


class UserVideosListView(generics.ListAPIView):
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated, CanAccessPrivateContent]
    pagination_class = VideoPagination
    ordering_fields = [
        "created_at",
        "updated_at",
    ]
    renderer_classes = [VideosJSONRenderer]

    def get_queryset(self):
        user = User.objects.get(id=self.kwargs.get("id"))
        user_videos = Video.objects.filter(user=user)
        return user_videos


class VideoCreateView(generics.CreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [VideoJSONRenderer]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

        video_creator = Profile.objects.get(user=self.request.user)
        followers = video_creator.followers.all()

        # Notify followers by email
        send_video_creation_notification(video_creator, followers)


class VideoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly,
        CanAccessPrivateContent,
    ]
    lookup_field = "id"
    renderer_classes = [VideoJSONRenderer]
    parser_classes = [MultiPartParser, FormParser]

    def perform_update(self, serializer):
        instance = serializer.save(user=self.request.user)
        if "thumbnail" in self.request.FILES:
            if (
                instance.thumbnail
                and instance.thumbnail.name != "/video_thumbnail_placeholder.png"
            ):
                default_storage.delete(instance.thumbnail.path)
            instance.thumbnail = self.request.FILES["thumbnail"]
            instance.save()

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()

        except Http404:
            raise VideoNotFoundException()

        serializer = self.get_serializer(instance)

        viewer_ip = request.META.get("REMOTE_ADDR", None)
        VideoView.record_view(video=instance, user=request.user, viewer_ip=viewer_ip)

        return Response(serializer.data)
