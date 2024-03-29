# Generated by Django 3.1.2 on 2020-10-18 13:49

import django_extensions.db.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_mri', '0009_auto_20200929_0818'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataDirectory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('path', models.FilePathField(allow_files=False, allow_folders=True)),
                ('known_subdirectories', models.JSONField(default=list)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
