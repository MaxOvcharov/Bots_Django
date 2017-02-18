# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models


class Cities(models.Model):
    city_name = models.CharField(max_length=40, verbose_name="Название города")
    city_url = models.TextField(verbose_name="Ссылка на город")
    author = models.CharField(max_length=60, verbose_name="Автор фотографий")

    def __str__(self):
        return "%s %s" % (self.city_name, self.author)

    class Meta:
        db_table = 'cities'
        ordering = ["city_name"]
        verbose_name = "Города"


class CityPhotos(models.Model):
    photo_url = models.TextField(verbose_name="Ссылка на фото")
    city_id = models.ForeignKey(Cities, on_delete=models.CASCADE, verbose_name="ID города")

    def __str__(self):
        return self.photo_url

    class Meta:
        db_table = 'city_photos'
        verbose_name = "Города"
