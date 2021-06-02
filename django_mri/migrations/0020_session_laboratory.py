# Generated by Django 3.2.3 on 2021-06-02 09:53

from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion

Laboratory = getattr(settings, "LABORATORY_MODEL", "accounts.Laboratory")


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(Laboratory),
        ("django_mri", "0019_alter_scan_study_groups"),
    ]

    operations = [
        migrations.AddField(
            model_name="session",
            name="laboratory",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="mri_session_set",
                to="accounts.laboratory",
            ),
        ),
    ]
