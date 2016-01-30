# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-30 17:51
from __future__ import unicode_literals

from django.db import migrations, models
import hunt.models


class Migration(migrations.Migration):

    dependencies = [
        ('hunt', '0006_auto_20160130_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='default.png', upload_to=hunt.models.Profile.get_upload_path),
        ),
    ]