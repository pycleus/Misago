# Generated by Django 4.2.10 on 2025-01-08 20:07

from django.db import migrations

from ..operations import CreateSetting


class Migration(migrations.Migration):

    dependencies = [
        ("misago_conf", "0016_add_flood_control_setting"),
    ]

    operations = [
        CreateSetting(
            setting="attachment_image_max_width",
            python_type="int",
            dry_value=3840,
        ),
        CreateSetting(
            setting="attachment_image_max_height",
            python_type="int",
            dry_value=2160,
        ),
        CreateSetting(
            setting="attachment_thumbnail_width",
            python_type="int",
            dry_value=1280,
        ),
        CreateSetting(
            setting="attachment_thumbnail_height",
            python_type="int",
            dry_value=720,
        ),
    ]
