# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-15 07:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_delete_textcontent'),
    ]

    operations = [
        migrations.CreateModel(
            name='TextContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.FileField(null=True, upload_to='files')),
            ],
            options={
                'verbose_name': 'TextContent',
                'verbose_name_plural': 'TextContents',
            },
        ),
    ]
