# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-20 07:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cities',
            name='city_name',
            field=models.CharField(max_length=40, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0433\u043e\u0440\u043e\u0434\u0430'),
        ),
    ]
