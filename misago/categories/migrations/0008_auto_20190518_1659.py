# Generated by Django 2.2.1 on 2019-05-18 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("misago_categories", "0007_best_answers_roles")]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="level",
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name="category",
            name="lft",
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name="category",
            name="rght",
            field=models.PositiveIntegerField(editable=False),
        ),
    ]