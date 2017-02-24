# -*- coding: utf-8 -*-

import telebot

from django.contrib.auth.models import User, Group
from django.views.generic import View
from TelegramBot.settings import BOT_TOKEN

from models import Cities, CityPhotos
from rest_framework import viewsets
from rest_framework.decorators import api_view
from serializers import UserSerializer, GroupSerializer, CityNamesSerializer, CityPhotosSerializer

bot = telebot.TeleBot(BOT_TOKEN)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CitiesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tests to be viewed or edited.
    """
    queryset = Cities.objects.all().order_by('city_name')
    serializer_class = CityNamesSerializer


class CityPhotosViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tests to be viewed or edited.
    """
    queryset = CityPhotos.objects.all().order_by('city_id')
    serializer_class = CityPhotosSerializer


@api_view(['POST'])
class CommandReceiveView(View):

    # Handle '/start' and '/help'
    @bot.message_handler(commands=['help', 'start'])
    def send_welcome(self, message):
        bot.reply_to(message,
                     ("Hi there, I am EchoBot.\n"
                      "I am here to echo your kind words back to you."))