# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-14 04:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20160114_0314'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExternalLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external', models.URLField()),
                ('internal', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name_plural': 'ExternalLinks',
                'verbose_name': 'ExternalLink',
            },
        ),
        migrations.AddField(
            model_name='headline',
            name='smart_link',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
