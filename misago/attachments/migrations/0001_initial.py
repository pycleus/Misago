# Generated by Django 4.2.10 on 2024-09-07 10:58

from django.conf import settings
import django.contrib.postgres.fields
import django.contrib.postgres.indexes
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import misago.attachments.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("misago_threads", "0014_plugin_data"),
        ("misago_acl", "0004_cache_version"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="AttachmentType",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("extensions", models.CharField(max_length=255)),
                ("mimetypes", models.CharField(blank=True, max_length=255, null=True)),
                ("size_limit", models.PositiveIntegerField(default=1024)),
                (
                    "status",
                    models.PositiveIntegerField(
                        choices=[
                            (0, "Allow uploads and downloads"),
                            (1, "Allow downloads only"),
                            (2, "Disallow both uploading and downloading"),
                        ],
                        default=0,
                    ),
                ),
                (
                    "limit_downloads_to",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.PositiveIntegerField(),
                        default=list,
                        size=None,
                    ),
                ),
                (
                    "limit_uploads_to",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.PositiveIntegerField(),
                        default=list,
                        size=None,
                    ),
                ),
                ("plugin_data", models.JSONField(default=dict)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Attachment",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="misago_threads.post",
                    ),
                ),
                (
                    "uploader",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("uploader_name", models.CharField(max_length=255)),
                ("uploader_slug", models.CharField(max_length=255)),
                (
                    "uploaded_at",
                    models.DateTimeField(
                        db_index=True, default=django.utils.timezone.now
                    ),
                ),
                ("secret", models.CharField(max_length=64)),
                (
                    "filetype",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="misago_attachments.attachmenttype",
                    ),
                ),
                ("filename", models.CharField(db_index=True, max_length=255)),
                ("size", models.PositiveIntegerField(db_index=True, default=0)),
                (
                    "thumbnail",
                    models.ImageField(
                        blank=True,
                        max_length=255,
                        null=True,
                        upload_to=misago.attachments.models.upload_to,
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        max_length=255,
                        null=True,
                        upload_to=misago.attachments.models.upload_to,
                    ),
                ),
                (
                    "video",
                    models.FileField(
                        blank=True,
                        max_length=255,
                        null=True,
                        upload_to=misago.attachments.models.upload_to,
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        blank=True,
                        max_length=255,
                        null=True,
                        upload_to=misago.attachments.models.upload_to,
                    ),
                ),
                ("plugin_data", models.JSONField(default=dict)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddIndex(
            model_name="attachment",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["plugin_data"], name="misago_atta_plugin__305a3d_gin"
            ),
        ),
        migrations.AddIndex(
            model_name="attachmenttype",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["plugin_data"], name="misago_atta_plugin__d2f0d1_gin"
            ),
        ),
    ]
