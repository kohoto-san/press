# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-14 02:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='headline',
            name='cycle',
        ),
        migrations.RemoveField(
            model_name='headline',
            name='media',
        ),
        migrations.DeleteModel(
            name='Headline',
        ),
        migrations.DeleteModel(
            name='HeadlineCycle',
        ),
        migrations.DeleteModel(
            name='Media',
        ),
    ]
