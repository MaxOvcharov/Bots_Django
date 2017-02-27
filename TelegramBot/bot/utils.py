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
    btn1 = types.KeyboardButton('Ввести название города')
    btn2 = types.KeyboardButton('Определить по Вашим геоданным', request_location=True)
    btn3 = types.KeyboardButton('Показать случайный')
    markup.add(btn1, btn2, btn3)

    return markup


def help_keyboard_handler(message):
    """
        Handle pressed button on first step of conversation.
        :param message: input message
    """

    if message.location:
        logger.debug(message.location)
        geo_data = geocoder.google([message.location['latitude'],
                                    message.location['longitude']],
                                   method='reverse')
        city_name = geo_data.city
        bot.send_message(message.chat.id, get_city_en(city_name))

    elif message.text == u'Показать случайный':
        # func3()
        pass

    else:
        logger.debug(message.text)
        lst_city_photos = get_city_ru(message.text)
        bot.send_message(message.chat.id, lst_city_photos)


def get_city_ru(city_name):
    """
        Get photos by city name(english version)
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
        city = Cities.objects.get(city_name=city_name)
        return 'City name: {0}, City URL: {1}, Author of photos: {2}'\
               .format(city.city_name, city.city_url, city.author)
    except Cities.DoesNotExist:
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
