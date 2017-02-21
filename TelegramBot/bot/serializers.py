# -*- coding: utf-8 -*-

from django.contrib.auth.models import User, Group
from bot.models import Cities, CityPhotos
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class CityNamesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cities
        fields = ('city_name', 'city_url', 'author')


class CityPhotosSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CityPhotos
        fields = ('city_id', 'photo_url', )

