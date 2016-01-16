# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-16 06:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20160114_1029'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('text', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'NewContacts',
                'verbose_name': 'NewContact',
            },
        ),
        migrations.DeleteModel(
            name='Contact',
        ),
    ]