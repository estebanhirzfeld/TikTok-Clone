from rest_framework.exceptions import ValidationError
from PIL import Image
from django.utils.translation import gettext_lazy as _


def validate_thumbnail_image_format(value):
    try:
        allowed_extensions = ['JPEG', 'JPG', 'WEBP', 'PNG']
        image = Image.open(value)
        if image.format.upper() not in allowed_extensions:
            raise ValueError(_("Invalid image format. Supported formats are JPEG, JPG, WEBP, and PNG."))
    except Exception as e:
        raise ValueError(_("Upload a valid image. The file you uploaded was either not an image or a corrupted image."))

def validate_video_format(value):
    # Check the file extension to ensure it's a valid video format
    allowed_extensions = ['MP4', 'AVI', 'MKV', 'MOV']
    file_extension = value.name.split('.')[-1].upper()

    if file_extension not in allowed_extensions:
        raise ValidationError(_("Invalid video file format. Only .MP4, .AVI, .MKV, .MOV files are allowed."))
    

def validate_video_size(value):
    max_size = 50 * 1024 * 1024  # 50 MB in bytes

    if value.size > max_size:
        raise ValidationError(_("Video size exceeds the maximum allowed size of 50 MB."))