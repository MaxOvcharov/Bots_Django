# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-16 13:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0003_auto_20170316_1302'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='citypoll',
            name='city',
        ),
        migrations.RemoveField(
            model_name='citypoll',
            name='user',
        ),
        migrations.RemoveField(
            model_name='cities',
            name='city_prefer',
        ),
        migrations.DeleteModel(
            name='CityPoll',
        ),
    ]
