import django_filters as filters

from apps.videos.models import Video


class VideoFilter(filters.FilterSet):
    user = filters.CharFilter(field_name="user__first_name", lookup_expr="icontains")
    tags = filters.CharFilter(field_name="tags__name", lookup_expr="iexact")
    description = filters.CharFilter(field_name="description", lookup_expr="icontains")
    created_at = filters.DateFromToRangeFilter(field_name="created_at")
    updated_at = filters.DateFromToRangeFilter(field_name="updated_at")

    class Meta:
        model = Video
        fields = ["user", "tags", "description", "created_at", "updated_at"]
