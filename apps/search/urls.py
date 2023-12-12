from django.urls import path

from .views import VideoElasticSearchView

urlpatterns = [
    path(
        "",
        VideoElasticSearchView.as_view({"get": "list"}),
        name="article_search",
    )
]
