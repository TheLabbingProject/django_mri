# Generated by Django 3.1.3 on 2021-04-20 13:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_mri', '0017_auto_20210318_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='irb',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='django_mri.irbapproval', verbose_name='IRB approval'),
        ),
    ]
