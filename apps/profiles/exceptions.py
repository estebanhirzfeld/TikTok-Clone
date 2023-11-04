from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException

class CantFollowYourself(APIException):
    status_code = 403
    default_detail = _("You can't follow yourself.")
    default_code = "forbidden"
