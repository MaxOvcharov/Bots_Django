# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import geocoder
import logging

from models import Cities, CityPhotos

logger = logging.getLogger('telegram')


class CityPhotoDialog(object):
    def __init__(self, bot):
        super(CityPhotoDialog, self).__init__()

        self.bot = bot

    def city_photo_dialog_handler(self, message):
        """
        Handle next step of conversation after command input.
        :param message: message from main view
        :return: None
        """
        try:
            logger.debug("CITY_PHOTO_STEP1: {}\n".format(message.text))
            if message.text == 'Определить по Вашим геоданным':
                logger.debug("LOCATION: {}\n\n\n".format(message.location))
                geo_data = geocoder.yandex([message.location.latitude,
                                            message.location.longitude],
                                           method='reverse')
                city_name = str(geo_data.city).encode('utf-8')
                logger.debug(city_name)
                res = self.get_city_en(city_name)
                logger.debug(res)
                self.bot.send_message(message.chat.id, res)

            elif message.text == 'Показать случайный':
                logger.debug('RANDOM_CITY: {}\n\n\n'.format(message.text))
                self.bot.send_message(message.chat.id, self.get_random_city)
            elif not str(message.text).startswith('/'):
                logger.debug("HANDLE_CITY: {}\n\n\n".format(message.text))
                lst_city_photos = self.get_city_ru(message.tex.encode('utf8', errors='replace'))
                self.bot.send_message(message.chat.id, lst_city_photos)
            else:
                logger.debug("Bad news!!!!!")
        except Exception as e:
            logger.debug(e)

    @property
    def get_random_city(self):
        """
            Get photos by random city ID
            :return: string of photos URLs
        """
        try:
            city = Cities.objects.random()
            return 'City name: {0}, City URL: {1}, Author of photos: {2}' \
                .format(city.city_name, city.city_url, city.author)
        except Exception as e:
            logger.debug('Handle ERROR: {0}'.format(e))
            return 'К сожалению нет такого города... :('

    @staticmethod
    def get_city_ru(city_name):
        """
            Get photos by city name(RU version)
            :param city_name:
            :return: string of photos URLs
        """
        try:
            logger.debug("CITY_RU: {0}-{1}".format(city_name, type(city_name)))
            city = Cities.objects.get(city_name=city_name)
            return 'City name: {0}, City URL: {1}, Author of photos: {2}'\
                   .format(city.city_name, city.city_url, city.author)
        except Cities.DoesNotExist:
            return 'К сожалению нет такого города... :('

    @staticmethod
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
        except Cities.DoesNotExist as e:
            logger.debug("Handle ERROR: {0}".format(e))
            return 'К сожалению нет такого города... :('

