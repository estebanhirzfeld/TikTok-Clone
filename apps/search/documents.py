from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from apps.videos.models import Video


@registry.register_document
class VideoDocument(Document):
    video_id = fields.KeywordField(attr="id")
    user_first_name = fields.TextField()
    user_last_name = fields.TextField()
    tags = fields.KeywordField(multi=True)
    thumbnail = fields.TextField(attr="thumbnail.url")
    is_private = fields.BooleanField(attr="user.profile.is_private")

    class Index:
        name = "videos"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Video
        fields = ["created_at"]

    def prepare_video_id(self, instance):
        return str(instance.id)

    def prepare_user_first_name(self, instance):
        return instance.user.first_name

    def prepare_user_last_name(self, instance):
        return instance.user.last_name

    def prepare_tags(self, instance):
        return [tag.name for tag in instance.tags.all()]
