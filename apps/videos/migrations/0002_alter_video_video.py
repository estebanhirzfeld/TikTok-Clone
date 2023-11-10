# Generated by Django 4.1.7 on 2023-11-07 17:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("videos", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="video",
            name="video",
            field=models.FileField(
                upload_to="",
                validators=[
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=["MOV", "avi", "mp4", "webm", "mkv"]
                    )
                ],
                verbose_name="video",
            ),
        ),
    ]