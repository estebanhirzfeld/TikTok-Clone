# Generated by Django 4.1.7 on 2023-11-15 19:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("profiles", "0002_remove_profile_followers_profile_following"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="is_private",
            field=models.BooleanField(default=False, verbose_name="is profile private"),
        ),
    ]
