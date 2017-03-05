# -*- coding: utf-8 -*-

import telebot
import logging
import geocoder

from django.contrib.auth.models import User, Group
from TelegramBot.settings import BOT_TOKEN

from city_photo_dialog import city_photo_dialog_handler, get_city_en, get_city_ru, get_random_city
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
            update = telebot.types.Update.de_json(data)
            bot.process_new_updates([update])
        except ValueError:
            return Response('Wrong data in json', status=status.HTTP_400_BAD_REQUEST)

        try:
            if dialog_data['command'].startswith('/') and \
                            dialog_data['step'] == 0:

                logger.debug('DIALOG: {}\n'.format(dialog_data))
                logger.debug('CONTEXT: {}\n'.format(context))

                # Handle '/help' command
                @bot.message_handler(commands=['help'])
                def send_help_info(message):
                    logger.info('HELP: {0}\n\n\n'.format(message.chat.id))
                    bot.send_message(message.chat.id,
                                     ("MaxTravelBot - это Ваш личный помощник в путешествии.\n"
                                      "Введите любой город России и получите ТОП-10 фото\n"
                                      "достопримечательностей города."))

                # Handle '/start' command
                @bot.message_handler(commands=['start'])
                def send_welcome(message):
                    logger.info('START: {0}\n\n\n'.format(message.chat.id))
                    markup = keyboards.markup_city_finder()
                    bot.send_message(message.chat.id,
                                     ("Привет, я твой личный помощник и могу показать\n"
                                      "тебе интересные места в городе.\n"
                                      "Какой город мне найти?"), reply_markup=markup)
                    DialogStepRouting.objects.next_step(dialog_data['chat_id'])

                # Handle '/city' command
                @bot.message_handler(commands=['photo'])
                def send_photo(message):
                    logger.info('PHOTO: {0}\n\n\n'.format(message.chat.id))
                    markup = keyboards.markup_city_finder()
                    bot.send_message(message.chat.id, "Какое фото мне загрузить?", reply_markup=markup)
                    DialogStepRouting.objects.next_step(dialog_data['chat_id'])

                @bot.message_handler(commands=['city'])
                def send_city_name(message):
                    logger.info('CITY: {0}\n\n\n'.format(message.chat.id))
                    markup = keyboards.markup_city_finder()
                    bot.send_message(message.chat.id, "Какой город мне найти?", reply_markup=markup)
                    DialogStepRouting.objects.next_step(dialog_data['chat_id'])

            elif dialog_data['command'] in (u'/start', u'/city', u'/photo')\
                    and dialog_data['step'] > 0:
                logger.debug('DIALOG: {}\n'.format(dialog_data))
                logger.debug('CONTEXT: {}\n'.format(context))

                @bot.message_handler(func=lambda m: True)
                def send_reply_all(message):
                    logger.info('ECHO: {0}\n\n\n'.format(message.chat.id))
                    bot.send_message(message.chat.id, message.text)
                    DialogStepRouting.objects.filter(chat_id=dialog_data['chat_id']).update(step=0)



            # city_photo_dialog_handler(data, dialog_data['step'])

            # @bot.message_handler(func=lambda m: True and dialog_data['step'] == 1)
            # def send_photos(message):
            #     logger.debug("CITY_PHOTO: {}\n\n\n".format(message.text))
            #     if message.location:
            #         logger.debug(message.location)
            #         geo_data = geocoder.yandex([message.location.latitude,
            #                                     message.location.longitude],
            #                                    method='reverse')
            #         city_name = str(geo_data.city).encode('utf-8')
            #         logger.debug(city_name)
            #         res = get_city_en(city_name)
            #         logger.debug(res)
            #         bot.send_message(message.chat.id, res)
            #
            #     elif message.text == u'Показать случайный':
            #         logger.debug(u'Показать случайный - OK')
            #         bot.send_message(message.chat.id, get_random_city())
            #
            #     elif not str(message.text).startswith('/'):
            #         logger.debug(message.text)
            #         lst_city_photos = get_city_ru(message.text)
            #         bot.send_message(message.chat.id, lst_city_photos)
            #     else:
            #         logger.debug("Bad news!!!!!")

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


