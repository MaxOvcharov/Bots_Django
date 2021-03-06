# -*- coding: utf-8 -*-

import telebot
import logging
import botan

from django.contrib.auth.models import User, Group
from TelegramBot.settings import BOT_TOKEN, BOTAN_API_KEY
from django.db.models import F

from cityPhotoDialog import CityPhotoDialog
from context_handler import ContextHandler
from models import Cities, CityPhotos, DialogStepRouting, CityPoll, NewsPoll, News
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from small_talk import small_talk
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
        logger.debug('HELP: {0}\n\n\n'.format(message.chat.id))
        bot.send_message(message.chat.id,
                         ("MaxTravelBot - Ваш личный помощник\n"
                          "в путешествиях по России.\n"
                          "Введите любой город России и получите\n"
                          "ТОП-10 фото достопримечательностей города.\n"
                          "Доступные команды:\n"
                          "/start - начало диалога с ботом;\n"
                          "/city - показать фото нужного города;\n"))
        botan.track(BOTAN_API_KEY, message.chat.id, message, name="help_command")

    # Handle '/start' command
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        logger.debug('START: {0}\n\n\n'.format(message.chat.id))
        markup = keyboards.markup_city_finder()
        bot.send_message(message.chat.id,
                         ("Привет, я твой личный помощник и могу\n"
                          "показать тебе интересные места в городе.\n"
                          "Какой город мне найти?"), reply_markup=markup)
        DialogStepRouting.objects.filter(chat_id=message.chat.id).update(step=F('step') + 1)

    # Handle '/city' command
    @bot.message_handler(commands=['city'])
    def send_city_name(message):
        logger.debug('CITY: {0}\n\n\n'.format(message.chat.id))
        markup = keyboards.markup_city_finder()
        bot.send_message(message.chat.id, "Какой город мне найти?", reply_markup=markup)
        DialogStepRouting.objects.filter(chat_id=message.chat.id).update(step=F('step') + 1)

    # Handle second step of /city and /start commands
    @bot.message_handler(func=lambda m: True and dialog_data['step'] == 1,
                         content_types=['text', 'location'])
    def send_city_photo(message):
        logger.debug('GET_CITY_PHOTO: {0}\n'.format(message.chat.id))
        get_city_photo.city_photo_dialog_handler(message)
        DialogStepRouting.objects.filter(chat_id=message.chat.id).update(step=0)

    # Handle small talk via Api.ai
    @bot.message_handler(func=lambda m: True, content_types=['text'])
    def send_city_photo(message):
        logger.debug('SMALL_TALK: {0}\n'.format(message.chat.id))
        bot.send_message(message.chat.id, small_talk(message.text))

    # Handle city vote callback
    @bot.callback_query_handler(func=lambda call: call.data.startswith(u"like_"))
    def callback_inline_city_vote(call):
        city_name = call.data.split("_")[1]
        # Check is user already voted
        already_voted = CityPoll.objects.filter(city__city_name_en=city_name,
                                                user__chat_id=call.message.chat.id,
                                                like=True)
        logger.debug('CITY_VOTE: city:{0}, already voted:{1}\n'.format(city_name, already_voted))
        if not already_voted and city_name:
            like_num = CityPhotoDialog.get_city_like_num(city_name)
            inline_markup = keyboards.inline_city_vote(like=True, like_num=like_num)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Спасибо, нам очень приятно \xF0\x9F\x92\x8C",
                                  reply_markup=inline_markup)
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="Спасибо, нам очень приятно \xF0\x9F\x92\x8C")
            # Save the result of polling
            CityPhotoDialog.save_ciy_poll(city_name=city_name, chat_id=call.message.chat.id)
        elif already_voted or not city_name:
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="Извините, Вы уже проголосовали")

    # Handle news vote callback
    @bot.callback_query_handler(func=lambda call: call.data.startswith(u"news_like_"))
    def callback_inline_news_vote(call):
        news_id = call.data.split("_")[-1]
        # Check is user already voted
        already_voted = NewsPoll.objects.filter(news__id=news_id,
                                                user__chat_id=call.message.chat.id,
                                                like=True)
        logger.debug('NEWS_VOTE: news_id:{0}, already voted:{1}\n'.format(news_id, already_voted))
        if not already_voted and news_id:
            like_num = CityPhotoDialog.get_news_like_num(news_id)
            inline_markup = keyboards.inline_news_vote(like=True,
                                                       like_num=like_num[0],
                                                       news_id=news_id)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=like_num[1],
                                  reply_markup=inline_markup,
                                  parse_mode="HTML")
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="Спасибо, нам очень приятно \xF0\x9F\x92\x8C")
            # Save the result of polling
            CityPhotoDialog.save_news_poll(news_id=news_id, chat_id=call.message.chat.id)
        elif already_voted or not news_id:
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="Извините, Вы уже проголосовали")

except Exception as e:
    logger.error('Handle ERROR: {0}'.format(e))


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


