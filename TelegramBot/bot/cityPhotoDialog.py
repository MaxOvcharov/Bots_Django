# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import geocoder
import logging
from keyboards import markup_hider

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
            if message.text == 'Показать любой':
                city_data = self.get_random_city
                logger.debug('RANDOM_CITY: {0} - {1}\n\n\n'.format(city_data[0], city_data[1]))
                for photo_url in city_data[0][0:5]:
                    self.bot.send_photo(message.chat.id, open(photo_url, 'rb'), caption=city_data[1])
                    #self.bot.send_message(message.chat.id, photo_url)
            elif message.text and not message.text.startswith('/'):
                logger.debug("HANDLE_CITY: {}\n\n\n".format(message.text))
                lst_city_photos = self.get_city_ru(message.text)
                self.bot.send_message(message.chat.id, lst_city_photos)
            elif message.location:
                logger.debug("LOCATION: {}\n\n\n".format(message.location))
                geo_data = geocoder.yandex([message.location.latitude,
                                            message.location.longitude],
                                           method='reverse')
                city_name = str(geo_data.city).encode('utf-8')
                res = self.get_city_en(city_name)
                self.bot.send_message(message.chat.id, res, reply_markup=markup_hider())
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
            city_photo = list(CityPhotos.objects.filter(city_id=city.id).values_list("photo_path", flat=True))
            logger.debug("PHOTOS: {}\n".format(", ".join(city_photo)))
            return city_photo, city.city_name
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

