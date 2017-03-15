# -*- coding: utf-8 -*-

import telebot
import logging

from django.contrib.auth.models import User, Group
from TelegramBot.settings import BOT_TOKEN
from django.db.models import F

from cityPhotoDialog import CityPhotoDialog
from context_handler import ContextHandler
from models import Cities, CityPhotos, DialogStepRouting
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from serializers import UserSerializer, GroupSerializer, CityNamesSerializer, CityPhotosSerializer
import keyboards

bot = telebot.TeleBot(BOT_TOKEN)
get_city_photo = CityPhotoDialog(bot)
logger = logging.getLogger('telegram')
dialog_data = {}


class CommandReceiveView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        """
            Handler of all telegram commands
        """
        global dialog_data
        try:
            data = request.data
            context = ContextHandler(data)
            dialog_data = context.context_serializer()
            update = telebot.types.Update.de_json(data)
            bot.process_new_updates([update])
            logger.debug('DIALOG: {}\n'.format(dialog_data))
            logger.debug('CONTEXT: {}\n'.format(context))
            return Response(status=status.HTTP_200_OK)
        except ValueError:
            return Response('Wrong data in json', status=status.HTTP_400_BAD_REQUEST)

try:
    # Handle '/help' command
    @bot.message_handler(commands=['help'])
    def send_help_info(message):
        logger.info('HELP: {0}\n\n\n'.format(message.chat.id))
        bot.send_message(message.chat.id,
                         ("MaxTravelBot - Ваш личный помощник\n"
                          "в путешествиях по России.\n"
                          "Введите любой город России и получите\n"
                          "ТОП-10 фото достопримечательностей города.\n"
                          "Доступные команды:\n"
                          "/start - начало диалога с ботом;\n"
                          "/city - показать фото нужного города;\n"))

    # Handle '/start' command
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        logger.info('START: {0}\n\n\n'.format(message.chat.id))
        markup = keyboards.markup_city_finder()
        bot.send_message(message.chat.id,
                         ("Привет, я твой личный помощник и могу\n"
                          "показать тебе интересные места в городе.\n"
                          "Какой город мне найти?"), reply_markup=markup)
        DialogStepRouting.objects.filter(chat_id=message.chat.id).update(step=F('step') + 1)

    # Handle '/city' command
    @bot.message_handler(commands=['city'])
    def send_city_name(message):
        logger.info('CITY: {0}\n\n\n'.format(message.chat.id))
        markup = keyboards.markup_city_finder()
        bot.send_message(message.chat.id, "Какой город мне найти?", reply_markup=markup)
        DialogStepRouting.objects.filter(chat_id=message.chat.id).update(step=F('step') + 1)

    # Handle second step of /city and /start commands
    @bot.message_handler(func=lambda m: True and dialog_data['step'] == 1,
                         content_types=['text', 'location'])
    def send_city_photo(message):
        logger.info('GET_CITY_PHOTO: {0}\n'.format(message.chat.id))
        get_city_photo.city_photo_dialog_handler(message)
        DialogStepRouting.objects.filter(chat_id=message.chat.id).update(step=0)

    # Handle vote callback
    @bot.callback_query_handler(func=lambda call: True)
    def callback_inline_vote(call):
        if call.data == "like":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Спасибо, нам очень приятно \xF0\x9F\x92\x8C")
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="Спасибо, нам очень приятно \xF0\x9F\x92\x8C")
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Спасибо, мы будет стараться лучше \xF0\x9F\x99\x8F")
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="Спасибо, мы будет стараться лучше \xF0\x9F\x99\x8F")

except Exception as e:
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


