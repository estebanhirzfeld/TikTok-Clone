from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException


class VideoNotFoundException(APIException):
    status_code = 404
    default_detail = _("Video not found.")
    default_code = "not_found"
