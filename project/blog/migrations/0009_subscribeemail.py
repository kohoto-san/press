# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-22 13:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20151219_0834'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscribeEmail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
            ],
            options={
                'verbose_name_plural': 'Emails',
                'verbose_name': 'Email',
            },
        ),
    ]
