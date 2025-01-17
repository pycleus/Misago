# Generated by Django 4.2.10 on 2025-01-06 13:04

from django.db import migrations

from ..filetypes import filetypes


def populate_attachments_thumbnails_sizes(apps, _):
    Attachment = apps.get_model("misago_attachments", "Attachment")

    queryset = Attachment.objects.exclude(thumbnail="").order_by("id")

    for attachment in queryset.iterator(chunk_size=50):
        thumbnail_size = attachment.thumbnail.size
        attachment.thumbnail_size = thumbnail_size
        attachment.save(update_fields=["thumbnail_size"])


class Migration(migrations.Migration):

    dependencies = [
        ("misago_attachments", "0005_attachment_populate_filetype_id"),
    ]

    operations = [
        migrations.RunPython(
            populate_attachments_thumbnails_sizes,
            migrations.RunPython.noop,
        ),
    ]
