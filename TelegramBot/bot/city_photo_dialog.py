# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import geocoder
import logging
import telebot

from models import Cities, CityPhotos
from TelegramBot.settings import BOT_TOKEN


logger = logging.getLogger('telegram')

bot = telebot.TeleBot(BOT_TOKEN)


def city_photo_dialog_handler(data, next_step):
    """
    Handle next step of conversation after command input.
    :param data: context for webhook
    :param next_step: next step of dialog
    :return: None
    """
    update = telebot.types.Update.de_json(data)
    bot.process_new_updates([update])
    
    @bot.message_handler(func=lambda m: True and next_step == 1)
    def send_welcome(message):
        if message.location:
            logger.debug(message.location)
            geo_data = geocoder.yandex([message.location.latitude,
                                        message.location.longitude],
                                       method='reverse')
            city_name = str(geo_data.city).encode('utf-8')
            logger.debug(city_name)
            res = get_city_en(city_name)
            logger.debug(res)
            bot.send_message(message.chat.id, res)

        elif message.text == u'Показать случайный':
            logger.debug(u'Показать случайный - OK')
            bot.send_message(message.chat.id, get_random_city())

        elif not str(message.text).startswith('/'):
            logger.debug(message.text)
            lst_city_photos = get_city_ru(message.text)
            bot.send_message(message.chat.id, lst_city_photos)


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

