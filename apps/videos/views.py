from django.core.files.storage import default_storage
from django.shortcuts import render
from django.http import Http404
from django.shortcuts import get_object_or_404
import logging
from .models import Video, VideoView
from .serializers import VideoSerializer
from .permissions import IsOwnerOrReadOnly
from .pagination import VideoPagination
from .filters import VideoFilter
from .renderers import VideoJSONRenderer, VideosJSONRenderer

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework import filters, generics, permissions, status

from .emails import send_video_creation_notification
from apps.profiles.models import Profile

from .exceptions import VideoNotFoundException

# Create your views here.

logger = logging.getLogger(__name__)


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
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
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
        VideoView.record_view(
            video=instance, user=request.user, viewer_ip=viewer_ip
        )

        return Response(serializer.data)
    