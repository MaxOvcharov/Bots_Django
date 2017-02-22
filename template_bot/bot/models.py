# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models


class Test(models.Model):
    test_name = models.CharField(max_length=80, verbose_name="Название теста")
    test_url = models.TextField(verbose_name="Ссылка на тест")
    author = models.CharField(max_length=60, verbose_name="Автор теста")

    def __unicode__(self):
        return "Test name: %s; Author: %s;" % (self.test_name, self.author)

    class Meta:
        db_table = 'test'
        ordering = ["test_name"]
        verbose_name_plural = "Тесты"