# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-20 07:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_name', models.CharField(max_length=60, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0433\u043e\u0440\u043e\u0434\u0430')),
                ('city_url', models.TextField(verbose_name='\u0421\u0441\u044b\u043b\u043a\u0430 \u043d\u0430 \u0433\u043e\u0440\u043e\u0434')),
                ('author', models.CharField(max_length=60, verbose_name='\u0410\u0432\u0442\u043e\u0440 \u0444\u043e\u0442\u043e\u0433\u0440\u0430\u0444\u0438\u0439')),
            ],
            options={
                'ordering': ['city_name'],
                'db_table': 'cities',
                'verbose_name': '\u0413\u043e\u0440\u043e\u0434\u0430',
            },
        ),
        migrations.CreateModel(
            name='CityPhotos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo_url', models.TextField(verbose_name='\u0421\u0441\u044b\u043b\u043a\u0430 \u043d\u0430 \u0444\u043e\u0442\u043e')),
                ('city_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.Cities', verbose_name='ID \u0433\u043e\u0440\u043e\u0434\u0430')),
            ],
            options={
                'db_table': 'city_photos',
                'verbose_name': '\u0424\u043e\u0442\u043e \u0433\u043e\u0440\u043e\u0434\u043e\u0432',
            },
        ),
    ]
