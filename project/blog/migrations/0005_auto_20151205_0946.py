# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-05 09:46
from __future__ import unicode_literals

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to=blog.models.Post.get_upload_path),
        ),
    ]
