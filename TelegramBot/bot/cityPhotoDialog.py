# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import geocoder
import logging
import telebot

from models import Cities, CityPhotos

logger = logging.getLogger('telegram')


class CityPhotoDialog(object):
    def __init__(self, bot):
        super(CityPhotoDialog, self).__init__()

        self.bot = bot

    def city_photo_dialog_handler(self):
        """
        Handle next step of conversation after command input.
        :param message: message from main view
        :return: None
        """
        try:

            @self.bot.message_handler(func=lambda mes: mes.text == 'Определить по Вашим геоданным',
                                      content_types=['location'])
            def send_city_photo_by_location(message):
                logger.info('LOCATION: {0}\n\n\n'.format(message.location))
                geo_data = geocoder.yandex([message.location.latitude,
                                            message.location.longitude],
                                           method='reverse')
                city_name = str(geo_data.city).encode('utf-8')
                logger.debug(city_name)
                res = self.get_city_en(city_name)
                logger.debug(res)
                self.bot.send_message(message.chat.id, res)

            @self.bot.message_handler(func=lambda mes: mes.text == 'Показать случайный',
                                      content_types=['text'])
            def send_city_photo_by_location(message):
                logger.info('Random city: {0}\n\n\n'.format(message.location))
                self.bot.send_message(message.chat.id, self.get_random_city)
            
            # logger.debug("CITY_PHOTO: {}\n\n".format(message.text))
            # if message.location:
            #     logger.debug(message.location)
            #     geo_data = geocoder.yandex([message.location.latitude,
            #                                 message.location.longitude],
            #                                method='reverse')
            #     city_name = str(geo_data.city).encode('utf-8')
            #     logger.debug(city_name)
            #     res = self.get_city_en(city_name)
            #     logger.debug(res)
            #     self.bot.send_message(message.chat.id, res)
            #
            # elif message.text == u'Показать случайный':
            #     logger.debug(u'Показать случайный - OK')
            #     self.bot.send_message(message.chat.id, self.get_random_city)
            #
            # elif not str(message.text).startswith('/'):
            #     logger.debug(message.text)
            #     lst_city_photos = self.get_city_ru(message.text)
            #     self.bot.send_message(message.chat.id, lst_city_photos)
            # else:
            #     logger.debug("Bad news!!!!!")
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
            logger.debug(city_name)  # TODO: Add location check
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

