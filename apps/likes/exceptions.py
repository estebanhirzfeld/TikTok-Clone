from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _

class VideoLikeException(APIException):
    status_code = 400
    default_detail = _("Video like exception occurred.")
    default_code = "video_like_error"

class VideoLikeAlreadyExistsException(VideoLikeException):
    status_code = 400
    default_detail = _("You already liked this video.")
    default_code = "video_like_already_exists"

class VideoLikeNotFoundException(VideoLikeException):
    status_code = 404
    default_detail = _("Video like not found.")
    default_code = "video_like_not_found"


class CommentLikeException(APIException):
    status_code = 400
    default_detail = _("Comment like exception occurred.")
    default_code = "comment_like_error"

class CommentLikeAlreadyExistsException(CommentLikeException):
    status_code = 400
    default_detail = _("You already liked this comment.")
    default_code = "comment_like_already_exists"

class CommentLikeNotFoundException(CommentLikeException):
    status_code = 404
    default_detail = _("Comment like not found.")
    default_code = "comment_like_not_found"
