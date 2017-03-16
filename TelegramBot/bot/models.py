# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from random import randint

from django.db import models
from django.db.models import Count
from django.db.models import F


class UserManager(models.Manager):
    """
        Useful user db-methods
    """
    def random(self):
        count = self.aggregate(ids=Count('id'))['ids']
        random_index = randint(0, count - 1)
        return self.all()[random_index]

    def next_step(self, chat_id):
        self.filter(chat_id=chat_id).update(step=F('step') + 1)


class UserInfo(models.Model):
    first_name = models.CharField(max_length=150, verbose_name="Имя пользователя")
    last_name = models.CharField(max_length=150, verbose_name="Фамилия пользователя")
    username = models.CharField(max_length=150, verbose_name="Логин пользователя")
    chat_id = models.IntegerField(db_index=True, verbose_name="Идентификационный номер чата")

    def __unicode__(self):
        return 'First name: %s; Last name: %s; Username: %s; Chat ID: %s' % \
               (self.first_name, self.last_name, self.username, self.chat_id)

    class Meta:
        db_table = 'user_info'
        verbose_name_plural = 'Список пользователей'


class Cities(models.Model):
    city_name = models.CharField(max_length=80, unique=True, db_index=True, verbose_name="Название города")
    city_name_en = models.CharField(max_length=80, unique=True, verbose_name="Английское название города")
    geo_latitude_min = models.FloatField(null=True, blank=True, default=0.0)
    geo_latitude_max = models.FloatField(null=True, blank=True, default=0.0)
    geo_longitude_min = models.FloatField(null=True, blank=True, default=0.0)
    geo_longitude_max = models.FloatField(null=True, blank=True, default=0.0)
    city_url = models.TextField(verbose_name="Ссылка на город")
    author = models.CharField(max_length=60, verbose_name="Автор фотографий")
    city_prefer = models.ManyToManyField(UserInfo, through='CityPoll',
                                         verbose_name="Связь городов с пользователями")
    # Adds random method
    objects = UserManager()

    def __unicode__(self):
        return "City name(en): %s; City name: %s; Author: %s;\n" \
               "Coordinate box[latitude: %s, %s; longitude: %s, %s]\n" \
               "City URL: %s" % \
               (self.city_name_en, self.city_name, self.author,
                self.geo_latitude_min, self.geo_latitude_max,
                self.geo_longitude_min, self.geo_longitude_max,
                self.city_url)

    class Meta:
        db_table = 'cities'
        ordering = ["city_name"]
        verbose_name_plural = "Города"


class CityPhotos(models.Model):
    photo_url = models.TextField(verbose_name="Ссылка на фото")
    photo_path = models.TextField(verbose_name="Локальный путь к файлу")
    city_id = models.ForeignKey(Cities, on_delete=models.CASCADE, verbose_name="ID Города")

    def __unicode__(self):
        return 'Photo URL: %s' % self.photo_url

    class Meta:
        db_table = 'city_photos'
        verbose_name_plural = "Фото городов"


class CityPoll(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name="ID Пользователя")
    city = models.ForeignKey(Cities, on_delete=models.CASCADE, verbose_name="ID Города")
    like = models.BooleanField(default=False, verbose_name="Нравится/Ненравится")

    def __unicode__(self):
        return "City ID: %s; User ID: %s; Like: %s;\n" % \
               (self.city, self.user, self.like)

    class Meta:
        db_table = 'city_poll'
        verbose_name_plural = "Голосовалка по городам"


class DialogStepRouting(models.Model):
    chat_id = models.IntegerField(db_index=True, verbose_name="Идентификационный номер чата")
    command = models.CharField(max_length=80, verbose_name="Текущая комманда")
    step = models.IntegerField(verbose_name="Номер шага")
    # Adds  method
    objects = UserManager()

    def __unicode__(self):
        return 'Chat ID: %s; Command: %s; Step number: %s' % \
               (self.chat_id, self.command, self.step)

    class Meta:
        db_table = 'dialog_step_routing'
        verbose_name_plural = 'Диалоги с пользователями'


