# -*- coding: utf-8 -*-

import telebot
import logging

from django.contrib.auth.models import User, Group
from TelegramBot.settings import BOT_TOKEN

from city_photo_dialog import city_photo_dialog_handler
from context_handler import ContextHandler
from models import Cities, CityPhotos, DialogStepRouting
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from serializers import UserSerializer, GroupSerializer, CityNamesSerializer, CityPhotosSerializer
import keyboards

bot = telebot.TeleBot(BOT_TOKEN)

logger = logging.getLogger('telegram')


class CommandReceiveView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        """
            Handler of all telegram commands
        """
        try:
            data = request.data
            context = ContextHandler(data)
            dialog_data = context.context_serializer()
        except ValueError:
            return Response('Wrong data in json', status=status.HTTP_400_BAD_REQUEST)

        try:
            if dialog_data['command'].startswith('/') and \
                            dialog_data['step'] == 0:

                update = telebot.types.Update.de_json(data)
                logger.info('WEBHOOK: {}\n'.format(data))
                bot.process_new_updates([update])

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
                    markup = keyboards.markup_city_finder()
                    bot.send_message(message.chat.id,
                                     ("Привет, я твой личный помощник и могу показать\n"
                                      "тебе интересные места в городе.\n"
                                      "Какой город мне найти?"), reply_markup=markup)
                    DialogStepRouting.objects.next_step(dialog_data['step'])

                # Handle '/city' command
                @bot.message_handler(commands=['city'])
                def send_city_photo(message):
                    logger.info('City: {0}'.format(message.chat.id))
                    markup = keyboards.markup_city_finder()
                    bot.send_message(message.chat.id, "Какой город мне найти?", reply_markup=markup)
                    DialogStepRouting.objects.next_step(dialog_data['step'])

            elif dialog_data['command'] in (u'/start', u'/city')\
                    and dialog_data['step'] > 0:
                city_photo_dialog_handler(data, dialog_data['step'])

            return Response(status=status.HTTP_200_OK)
        except Exception, e:
            logger.error(e)


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


