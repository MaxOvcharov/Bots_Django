# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import geocoder
import logging

from django.core.exceptions import ObjectDoesNotExist

from keyboards import markup_hider, inline_go_to_city_url, inline_city_vote
from models import Cities, CityPhotos, CityPoll, UserInfo, News, NewsPoll

logger = logging.getLogger('telegram')


class CityPhotoDialog(object):
    def __init__(self, bot):
        super(CityPhotoDialog, self).__init__()

        self.bot = bot
        self.bad_city_name_response = 'К сожалению нет такого города... :('

    def city_photo_dialog_handler(self, message):
        """
            Handle next step of conversation after command input.
            PS: city_data: tuple - 0:list(city_photo), 1:city_name,
                                   2:city.city_url, 3:city.city_name_en;
            :param message: message from main view;
            :return: None
        """
        try:
            logger.debug("CITY_PHOTO_STEP1: {}\n".format(message.text))
            if message.text == 'Показать любой':
                city_data = self.get_random_city
                logger.debug('RANDOM_CITY: {0} - {1}\n\n\n'.format(city_data[0],
                                                                   city_data[1]))
                if city_data:
                    self.send_city_photos(city_data, message)
                    like_num = self.get_city_like_num(city_data[3])
                    logger.debug("LIKE_NUM: {}\n\n\n".format(like_num))
                    self.bot.send_message(message.chat.id, "Вам понравилась информация?",
                                          reply_markup=inline_city_vote(like_num=like_num,
                                                                        city_name=city_data[3]))
                else:
                    # No one city was found
                    self.bot.send_message(message.chat.id, self.bad_city_name_response,
                                          repply_markup=markup_hider())

            elif message.text and not message.text.startswith('/'):
                logger.debug("HANDLE_CITY: {}\n\n\n".format(message.text))
                city_data = self.get_city_ru(message.text)
                if city_data:
                    self.send_city_photos(city_data, message)
                    like_num = self.get_city_like_num(city_data[3])
                    self.bot.send_message(message.chat.id, "Вам понравилась информация?",
                                          reply_markup=inline_city_vote(like_num=like_num,
                                                                        city_name=city_data[3]))
                else:
                    # No one city was found
                    self.bot.send_message(message.chat.id, self.bad_city_name_response,
                                          repply_markup=markup_hider())

            elif message.location:
                logger.debug("LOCATION: {}\n\n\n".format(message.location))
                geo_data = geocoder.yandex([message.location.latitude,
                                            message.location.longitude],
                                           method='reverse')
                city_name = str(geo_data.city).encode('utf-8')
                city_data = self.get_city_en(city_name)
                if city_data:
                    self.send_city_photos(city_data, message)
                    like_num = self.get_city_like_num(city_data[3])
                    self.bot.send_message(message.chat.id, "Вам понравилась информация?",
                                          reply_markup=inline_city_vote(like_num=like_num,
                                                                        city_name=city_data[3]))
                else:
                    # No one city was found
                    self.bot.send_message(message.chat.id, self.bad_city_name_response,
                                          repply_markup=markup_hider())

            else:
                logger.debug("Bad news!!!!!")
        except Exception as e:
            logger.error('Handle ERROR: {0}'.format(e))

    def send_city_photos(self, city_data, message):
        """
            This function sends city photos and the last
            photo sends with the URL of city
            :param city_data: tuple - 0:list(city_photo), 1:city_name,
                                      2:city.city_url, 3:city.city_name_en;
            :param message: message from telegram;
            :return: None
        """
        photo_urls = city_data[0][0:5]
        last_photo_num = len(photo_urls) - 1
        for i, photo_url in enumerate(photo_urls):
            if i != last_photo_num:
                self.bot.send_photo(message.chat.id, open(photo_url, 'rb'),
                                    caption=city_data[1],
                                    reply_markup=markup_hider())
            else:
                self.bot.send_photo(message.chat.id, open(photo_url, 'rb'),
                                    caption=city_data[1],
                                    reply_markup=inline_go_to_city_url(city_name=city_data[1],
                                                                       city_url=city_data[2]))

    @staticmethod
    def save_ciy_poll(city_name, chat_id):
        """
            Save the result of city poll
            :param city_name: city name(EN)
            :param chat_id: chat ID
            :return: None
        """
        try:
            logger.debug("SAVE CITY POLL: city name-{0},"
                         " chat_id-{1}".format(city_name, chat_id))
            user = UserInfo.objects.get(chat_id=chat_id)
            city = Cities.objects.get(city_name_en=city_name)
            city_poll = CityPoll.objects.create(user=user, city=city, like=True)
        except ObjectDoesNotExist, e:
            logger.error('Handle ERROR: {0}'.format(e))
        except Exception, e:
            logger.error('Handle ERROR: {0}'.format(e))

    @staticmethod
    def get_city_like_num(city_name):
        """
            Count number of likes for chosen city
            :param city_name: chosen city;
            :return: int - number of likes
        """
        return CityPoll.objects.filter(city__city_name_en=city_name, like=True).count()

    @staticmethod
    def save_news_poll(news_id, chat_id):
        """
            Save the result of news poll
            :param news_id: news ID
            :param chat_id: chat ID
            :return: None
        """
        try:
            logger.debug("SAVE NEWS POLL: news_id-{0},"
                         " chat_id-{1}".format(news_id, chat_id))
            user = UserInfo.objects.get(chat_id=chat_id)
            news = News.objects.get(id=news_id)
            news_poll = NewsPoll.objects.create(user=user, news=news, like=True)
        except ObjectDoesNotExist, e:
            logger.error('Handle ERROR: {0}'.format(e))
        except Exception, e:
            logger.error('Handle ERROR: {0}'.format(e))

    @staticmethod
    def get_news_like_num(news_id):
        """
            Count number of likes for chosen news
            and get news content
            :param news_id: news ID;
            :return: tuple: int - number of likes,
                            str - news content
        """
        likes = NewsPoll.objects.filter(news__id=news_id, like=True).count()
        news_content = News.objects.values_list('content', flat=True).get(pk=news_id)
        return likes, news_content

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
            return city_photo, city.city_name, city.city_url, city.city_name_en
        except Exception as e:
            logger.error('Handle ERROR: {0}'.format(e))
            return None

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
            city_photo = list(CityPhotos.objects.filter(city_id=city.id).values_list("photo_path", flat=True))
            return city_photo, city.city_name, city.city_url, city.city_name_en
        except Cities.DoesNotExist, e:
            logger.error('Handle ERROR: {0}'.format(e))
            return None

    @staticmethod
    def get_city_en(city_name):
        """
            Get photos by city name(english version)
            :param city_name:
            :return: string of photos URLs
        """
        try:
            city = Cities.objects.get(city_name_en=city_name)
            city_photo = list(CityPhotos.objects.filter(city_id=city.id).values_list("photo_path", flat=True))
            return city_photo, city.city_name, city.city_url, city.city_name_en
        except Cities.DoesNotExist as e:
            logger.error("Handle ERROR: {0}".format(e))
            return None

