# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from telebot import types


def markup_city_finder():
    """
        Generate keyboard - "City finder"
        :return: markup object
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, 
                                       one_time_keyboard=True,
                                       selective=True,
                                       row_width=1)
    # Create all buttons
    btn1 = types.KeyboardButton('Определить по Вашим геоданным', request_location=True)
    btn2 = types.KeyboardButton('Показать любой')
    markup.add(btn1, btn2)
    return markup


def markup_hider():
    markup = types.ReplyKeyboardRemove(True)
    return markup


def inline_go_to_city_url(city_name=None, city_url=None):
    """
        Inline keyboard with hyperlink to the city web-page
        :param city_name: city name(RU)
        :param city_url: city web-page
        :return: markup object
    """
    markup = types.InlineKeyboardMarkup()
    # Create all buttons
    city_url_button = types.InlineKeyboardButton(text="Перейти на страницу города: {0}".
                                                 format(city_name), url=city_url)
    markup.add(city_url_button)
    return markup


def inline_city_vote(like=False, like_num=0, city_name=""):
    """
        Inline keyboard with heart emoji and like-counter
        :param like: If user liked the city
        :param like_num: number of likes
        :param city_name: city name(EN)
        :return: markup object
    """
    markup = types.InlineKeyboardMarkup(row_width=1)
    # Create all buttons
    if like:
        #
        like_button = types.InlineKeyboardButton(text=u"\u2764 {0}".format(like_num + 1),
                                                 callback_data="like_{0}".format(city_name))
    else:
        # send default button
        like_button = types.InlineKeyboardButton(text=u"\u2764 {0}".format(like_num),
                                                 callback_data="like_{0}".format(city_name))
    markup.add(like_button)
    return markup


def inline_news_vote(like=False, like_num=0, news_id=0):
    """
        Inline keyboard with heart emoji and like-counter
        :param like: If user liked the news
        :param like_num: number of likes
        :param news_id: news ID
        :return: markup object
    """
    markup = types.InlineKeyboardMarkup(row_width=1)
    if like:
        like_button = types.InlineKeyboardButton(text=u"\u2764 {0}".format(like_num + 1),
                                                 callback_data="news_like_{0}".format(news_id))
    else:
        like_button = types.InlineKeyboardButton(text=u"\u2764",
                                                 callback_data="news_like_{0}".format(news_id))
    markup.add(like_button)
    return markup