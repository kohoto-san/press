# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-12 13:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_post_id_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id_post',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]