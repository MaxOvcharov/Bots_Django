# -*- coding: utf-8 -*-

import telebot
import logging
import time

from django.contrib.auth.models import User, Group
from TelegramBot.settings import BOT_TOKEN

from models import Cities, CityPhotos
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from serializers import UserSerializer, GroupSerializer, CityNamesSerializer, CityPhotosSerializer
import utils

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
        except ValueError:
            return Response('Wrong data in json', status=status.HTTP_400_BAD_REQUEST)
        else:
            update = telebot.types.Update.de_json(data)
            bot.process_new_updates([update])
            user_step = {}
        try:
            # Handle '/help' command
            @bot.message_handler(commands=['help'])
            def send_help_info(message):
                logger.info('HELP: {0}'.format(message.chat.id))
                bot.send_message(message.chat.id,
                                 ("MaxTravelBot - это Ваш личный помощник в путешествии.\n"
                                  "Введите любой город России и получите ТОП-10 фото\n"
                                  "достопримечательностей города."))

            # Handle '/start' command
            @bot.message_handler(commands=['start'])
            def send_welcome(message):
                logger.info('START: {0}'.format(message.chat.id))
                markup = utils.markup_city_finder()
                msg = bot.send_message(message.chat.id,
                                       ("Привет, я твой личный помощник и могу показать\n"
                                        "тебе интересные места в городе.\n"
                                        "Какой город мне найти?"), reply_markup=markup)
                bot.register_next_step_handler(msg, utils.help_keyboard_handler(user_step))
                time.sleep(1)
                user_step[message.chat.id] = 1

            @bot.message_handler(func=lambda message: utils.get_user_step(message.chat.id, user_step) == 1)
            def send_city_content(message):
                logger.info(message.text)
                lst_city_photos = utils.get_city(message.text)
                bot.send_message(message.chat.id, lst_city_photos)
                user_step[message.chat.id] = 0

            return Response(status=status.HTTP_200_OK)
        except Exception, e:
            logger.error(e)

    def get(self, request, format=None):
        return Response({"message": "Hello for today! See you tomorrow!"})
    


