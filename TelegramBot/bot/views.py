# -*- coding: utf-8 -*-

import telebot
import logging

from django.contrib.auth.models import User, Group
from TelegramBot.settings import BOT_TOKEN

from models import Cities, CityPhotos
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from serializers import UserSerializer, GroupSerializer, CityNamesSerializer, CityPhotosSerializer

bot = telebot.TeleBot(BOT_TOKEN)

logger = logging.getLogger('telegram')


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


class CommandReceiveView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        """
            Handler of all telegram commands
        """
        try:
            data = request.data
            logger.info('Get POST: {}'.format(data))
        except ValueError:
            return Response('Wrong data in json', status=status.HTTP_400_BAD_REQUEST)
        else:
            update = telebot.types.Update.de_json(data)
            bot.process_new_updates([update])
        try:
            # Handle '/start' and '/help'
            @bot.message_handler(commands=['help', 'start'])
            def send_welcome(message):
                bot.reply_to(message,
                             ("Hi there, I am EchoBot.\n"
                              "I am here to echo your kind words back to you."))
            return Response(status='200')
        except Exception, e:
            logger.error(e)

    def get(self, request, format=None):
        return Response({"message": "Hello for today! See you tomorrow!"})
