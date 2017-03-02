# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import geocoder
import logging
import telebot
from telebot import types

from models import Cities, CityPhotos
from TelegramBot.settings import BOT_TOKEN


logger = logging.getLogger('telegram')

bot = telebot.TeleBot(BOT_TOKEN)


def markup_city_finder():
    """
        Generate keyboard - "City finder"
        :return: markup object
    """
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                       resize_keyboard=True,
                                       row_width=1)
    # Create all buttons
    btn1 = types.KeyboardButton('Определить по Вашим геоданным', request_location=True)
    btn2 = types.KeyboardButton('Показать случайный')
    markup.add(btn1, btn2)

    return markup


def start_command_handler(message):
    """
        Handle pressed button on first step of conversation.
        :param message: input message
    """

    if message.location:
        logger.debug(message.location)
        geo_data = geocoder.yandex([message.location.latitude,
                                    message.location.longitude],
                                   method='reverse')
        city_name = str(geo_data.city).encode('utf-8')
        logger.debug(city_name)
        res = get_city_en(city_name)
        logger.debug(res)
        keyboard_hider = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, res, reply_markup=keyboard_hider)

    elif message.text == u'Показать случайный':
        keyboard_hider = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, get_random_city(),
                         reply_markup=keyboard_hider)

    elif not str(message.text).startswith('/'):
        logger.debug(message.text)
        lst_city_photos = get_city_ru(message.text)
        keyboard_hider = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, lst_city_photos,
                         reply_markup=keyboard_hider)


def get_random_city():
    """
            Get photos by random city ID
            :return: string of photos URLs
        """
    try:
        city = Cities.objects.random()
        return 'City name: {0}, City URL: {1}, Author of photos: {2}' \
            .format(city.city_name, city.city_url, city.author)
    except Exception, e:
        logger.debug('Handle ERROR: {0}'.format(e))
        return 'К сожалению нет такого города... :('


def get_city_ru(city_name):
    """
        Get photos by city name(RU version)
        :param city_name:
        :return: string of photos URLs
    """
    try:
        logger.debug(city_name)  # TODO: Add location check
        city = Cities.objects.get(city_name=city_name)
        return 'City name: {0}, City URL: {1}, Author of photos: {2}'\
               .format(city.city_name, city.city_url, city.author)
    except Cities.DoesNotExist:
        return 'К сожалению нет такого города... :('


def get_city_en(city_name):
    """
        Get photos by city name(english version)
        :param city_name:
        :return: string of photos URLs
    """
    try:
        city = Cities.objects.get(city_name_en=city_name)
        return 'City name: {0}, City URL: {1}, Author of photos: {2}'\
               .format(city.city_name, city.city_url, city.author)
    except Cities.DoesNotExist, e:
        logger.debug("Handle ERROR: {0}".format(e))
        return 'К сожалению нет такого города... :('


def get_user_step(uid, user_step):
    """
        Validate user step by user ID
        :param uid: chat ID
        :param user_step: Dict with the user_id and user_step
        :return: Step number
    """
    if uid in user_step:
        return user_step[uid]
    else:
        user_step[uid] = 0
        return 0
