from django_elasticsearch_dsl_drf.filter_backends import (
    DefaultOrderingFilterBackend,
    FilteringFilterBackend,
    IdsFilterBackend,
    OrderingFilterBackend,
    SearchFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from elasticsearch_dsl import Q
from rest_framework import permissions

from .documents import VideoDocument
from .serializers import VideoElasticSearchSerializer


class VideoElasticSearchView(DocumentViewSet):
    document = VideoDocument
    serializer_class = VideoElasticSearchSerializer
    lookup_field = "id"
    permission_classes = [permissions.AllowAny]

    filter_backends = [
        FilteringFilterBackend,
        IdsFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
    ]
    search_fields = (
        "description",
        "user_first_name",
        "user_last_name",
        "tags",
    )
    filter_fields = {"tags": "tags", "created_at": "created_at"}

    ordering_fields = {"created_at": "created_at"}
    ordering = ("-created_at",)

    def get_queryset(self):
        queryset = super().get_queryset()

        # Exclude videos where the user owner has profile.is_private = True
        exclude_private_user_query = ~Q("term", is_private=True)
        queryset = queryset.query(exclude_private_user_query)

        return queryset
