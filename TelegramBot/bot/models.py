# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models


class Cities(models.Model):
    city_name = models.CharField(max_length=80, verbose_name="Название города")
    city_url = models.TextField(verbose_name="Ссылка на город")
    author = models.CharField(max_length=60, verbose_name="Автор фотографий")

    def __unicode__(self):
        return "City name: %s; Author: %s;" % (self.city_name, self.author)

    class Meta:
        db_table = 'cities'
        ordering = ["city_name"]
        verbose_name_plural = "Города"


class CityPhotos(models.Model):
    photo_url = models.TextField(verbose_name="Ссылка на фото")
    city_id = models.ForeignKey(Cities, on_delete=models.CASCADE, verbose_name="ID города")

    def __unicode__(self):
        return 'Photo URL: %s' % (self.photo_url)

    class Meta:
        db_table = 'city_photos'
        verbose_name_plural = "Фото городов"