# Generated by Django 3.0.6 on 2020-08-13 01:18

from datetime import datetime

import django.db.models.deletion
import django_extensions.db.fields
from django.conf import settings
from django.db import IntegrityError, migrations, models, transaction


class Migration(migrations.Migration):
    dependencies = [
        ("django_mri", "0005_auto_20200727_0624"),
    ]

    operations = [
        migrations.CreateModel(
            name="Session",
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
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                (
                    "comments",
                    models.TextField(
                        blank=True,
                        help_text="General comments about MRI scanning session.",
                        max_length=1000,
                        null=True,
                    ),
                ),
                ("time", models.DateTimeField(default=datetime.now)),
                (
                    "subject",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="mri_session_set",
                        to=settings.SUBJECT_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("-modified", "-created"),
                "get_latest_by": "modified",
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="scan",
            name="session",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="django_mri.Session",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="scan", unique_together={("number", "session")},
        ),
    ]
